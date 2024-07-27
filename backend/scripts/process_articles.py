import os
import time
import requests
from bs4 import BeautifulSoup
import pinecone
from openai import OpenAI
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

index_name = "news-articles"

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=pinecone.ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to get GDELT data with rate limiting and retry logic
def get_gdelt_data(query, maxrecords=250, retries=5):
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&format=json&maxrecords={maxrecords}&lang=english"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    for i in range(retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                logging.error(f"Unable to parse JSON response. Response content: {response.content}")
                return {}
        elif response.status_code == 429:
            wait_time = 2 ** i  # Exponential backoff
            logging.warning(f"Rate limit exceeded. Retrying after {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            logging.error(f"Received status code {response.status_code} from GDELT API")
            return {}

    logging.error("Maximum retries reached. Exiting.")
    return {}

# Function to extract article URLs
def extract_article_urls(data):
    articles = data.get("articles", [])
    urls = [article.get("url") for article in articles]
    return urls

# Function to scrape article content
def scrape_article_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        logging.error(f"Error scraping content from {url}: {e}")
        return ""

# Function to get embeddings from OpenAI
def get_embeddings(text):
    try:
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Error getting embeddings: {e}")
        return []

# Function to store articles in Pinecone with checks
def store_article(url, content):
    # Check if content is in English
    try:
        if detect(content) != 'en':
            logging.info(f"Non-English content for URL {url}, skipping.")
            return False
    except LangDetectException:
        logging.info(f"Failed to detect language for URL {url}, skipping.")
        return False

    # Check for invalid content
    if "You don't have permission to access" in content or not content.strip() or "denied by UA ACL" in content or "Performance & security by Cloudflare" in content:
        logging.info(f"Invalid content for URL {url}, skipping.")
        return False

    # Get embeddings
    embedding = get_embeddings(content)
    if not embedding:
        logging.info(f"Failed to get embeddings for URL {url}, skipping.")
        return False

    # Store in Pinecone
    index.upsert([
        {"id": url, "values": embedding, "metadata": {"text": content}}
    ])
    logging.info(f"Stored article from URL {url}")
    return True

# Main function
def main():
    query = "climate change"
    stored_articles = 0
    maxrecords = 250  # Number of articles per request

    while stored_articles < 1000:  # Adjust this to store more articles
        data = get_gdelt_data(query, maxrecords)
        if not data:
            break  # Exit the loop if data is empty due to maximum retries reached

        urls = extract_article_urls(data)

        for url in urls:
            content = scrape_article_content(url)
            if content and store_article(url, content):
                stored_articles += 1
                logging.info(f"Stored articles count: {stored_articles}")
                if stored_articles >= 1000:  # Adjust to store desired number of articles
                    break

        maxrecords += 250  # Increase to fetch more articles in subsequent requests
        time.sleep(1)  # Add a delay between each iteration to avoid rate limits

    logging.info(f"Stored {stored_articles} articles.")

if __name__ == "__main__":
    main()
