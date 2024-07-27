import requests
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException
from sqlalchemy import create_engine, Column, Integer, String, Text, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up SQLAlchemy
engine = create_engine('sqlite:///news.db')
Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    content = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Step 1: Get GDELT Data
def get_gdelt_data(query, maxrecords=10):
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&format=json&maxrecords={maxrecords}&lang=english"
    response = requests.get(url)
    return response.json()

# Step 2: Extract URLs
def extract_article_urls(data):
    articles = data.get("articles", [])
    urls = [article.get("url") for article in articles]
    return urls

# Step 3: Scrape Content
def scrape_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([para.get_text() for para in paragraphs])
    return content

# Step 4: Store Articles
def store_article(url, content):
    if session.query(exists().where(NewsArticle.url == url)).scalar():
        print(f"Article with URL {url} already exists in the database.")
        return False

    # Skip articles with invalid content
    if "You don't have permission to access" in content or not content.strip() or "denied by UA ACL" or "Performance & security by Cloudflare" in content:
        print(f"Invalid content for URL {url}, skipping.")
        return False

    # Additional check for English language
    try:
        if detect(content) != 'en':
            print(f"Non-English content for URL {url}, skipping.")
            return False
    except LangDetectException:
        print(f"Failed to detect language for URL {url}, skipping.")
        return False

    article = NewsArticle(url=url, content=content)
    session.add(article)
    session.commit()
    return True

# Step 5: Retrieve Articles
def get_all_articles():
    return session.query(NewsArticle).all()

# Example usage:
def main():
    query = "climate change"
    stored_articles = 0
    maxrecords = 10  # Start with a higher number to account for invalid URLs

    while stored_articles < 3:
        data = get_gdelt_data(query, maxrecords)
        urls = extract_article_urls(data)

        for url in urls:
            content = scrape_article_content(url)
            # Validate content language if necessary
            if store_article(url, content):
                stored_articles += 1
                if stored_articles >= 3:  # Break the loop if we have stored 3 articles
                    break

        # Increase the number of records to fetch if not enough valid articles are found
        maxrecords += 10

    articles = get_all_articles()
    for article in articles:
        print(article.url, article.content)

if __name__ == "__main__":
    main()
