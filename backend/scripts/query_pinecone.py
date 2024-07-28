import os
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load your Pinecone API key
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not found. Make sure it's set in your .env file.")

pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Connect to your index
index_name = "news-articles"
index = pc.Index(index_name)

# Define the query strings you want to search for
query_strings = ["CAPTCHA", "text missing", "403 Forbidden", "Access Denied"]

# Function to perform query and return matching IDs
def query_records(query_string):
    response = index.query(
        vector=[0]*1536,  # Dummy vector; replace with actual vector if available
        top_k=1000,  # Increase this if you have more matching records
        include_metadata=True,
        filter={
            "text": {
                "$contains": query_string
            }
        }
    )
    return [match['id'] for match in response['matches']]


# Collect all matching record IDs
all_matching_ids = set()
for query_string in query_strings:
    matching_ids = query_records(query_string)
    all_matching_ids.update(matching_ids)
    print(f"Found {len(matching_ids)} records containing '{query_string}'")

# Print out the IDs and text of each matching record
for record_id in all_matching_ids:
    response = index.fetch([record_id])
    if record_id in response['vectors']:
        record_text = response['vectors'][record_id]['metadata']['text']
        print(f"ID: {record_id}\nText: {record_text[:200]}...\n")  # Print first 200 characters

# Confirm before deleting
confirm = input(f"Are you sure you want to delete {len(all_matching_ids)} records? (yes/no): ")

if confirm.lower() == 'yes':
    # Delete the matching records
    #index.delete(ids=list(all_matching_ids))
    print(f"Deleted {len(all_matching_ids)} records.")
else:
    print("Deletion cancelled.")