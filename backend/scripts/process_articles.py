import os
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import pinecone
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Initialize Pinecone
pc = pinecone.Pinecone(
    api_key=PINECONE_API_KEY
)

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

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Function to get GDELT data
def get_gdelt_data(query, maxrecords=250):
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&format=json&maxrecords={maxrecords}&lang=english"
    response = requests.get(url)
    return response.json()

# Function to extract article URLs
def extract_article_urls(data):
    articles = data.get("articles", [])
    urls = [article.get("url") for article in articles]
    return urls

# Function to scrape article content
def scrape_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([para.get_text() for para in paragraphs])
    return content

# Function to store articles in Pinecone
def store_article(url, content):
    if not content.strip():
        print(f"Invalid content for URL {url}, skipping.")
        return False
    
    inputs = tokenizer(content, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    
    index.upsert([(url, embeddings.tolist())])
    return True

# Main function
def main():
    query = "climate change"
    stored_articles = 0
    maxrecords = 250  # Increased to fetch more articles per request

    while stored_articles < 1000:  # Increase this to store more articles
        data = get_gdelt_data(query, maxrecords)
        urls = extract_article_urls(data)

        for url in urls:
            content = scrape_article_content(url)
            if store_article(url, content):
                stored_articles += 1
                if stored_articles >= 1000:  # Adjust this number to store the desired amount of articles
                    break

        maxrecords += 250  # Optionally increase to fetch even more articles in subsequent requests

    print(f"Stored {stored_articles} articles.")

if __name__ == "__main__":
    main()
