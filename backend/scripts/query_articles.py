import os
from transformers import AutoTokenizer, AutoModel
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import pinecone
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment='us-east-1')

index_name = "news-articles"
index = pinecone.Index(index_name)

# Initialize LangChain components
vector_store = Pinecone(index)

# Initialize the LLM with LangChain
llm = OpenAI(api_key=OPENAI_API_KEY)

# Create a retrieval-based QA chain
qa_chain = RetrievalQA(llm=llm, retriever=vector_store.as_retriever())

# Example query
query = "What are the latest developments in climate change?"
result = qa_chain.run(query)

print("Query:", query)
print("Answer:", result)
