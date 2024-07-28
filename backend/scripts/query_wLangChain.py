import os
import sys
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai.embeddings import OpenAIEmbeddings
from pinecone import Pinecone

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize the OpenAI model
model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")

# Initialize the output parser
parser = StrOutputParser()

# Define the prompt template for summarizing articles
template = """
You are a knowledgeable news assistant, tasked with providing concise and relevant summaries of current events. Use the following articles to answer the user's question:

Context: {context}

User's Question: {question}

Instructions:
1. Begin your response with a natural, conversational opener such as "Recent news reports indicate that..." or "According to the latest information...".
2. Directly address the user's question using insights from the provided articles.
3. Highlight only the most relevant and important information related to the question.
4. Use a neutral, informative tone throughout your response.
5. If the articles don't provide sufficient information to fully answer the question, acknowledge this and provide the best available information.
6. Include URLs for the articles you referenced where appropriate.
7. If applicable, summarize the key points of the articles in bullet points for clarity.
8. Provide additional context or background information if it helps in understanding the current event.

"""

prompt = ChatPromptTemplate.from_template(template)

# Initialize the embeddings model
embeddings = OpenAIEmbeddings()

# Print a newline for better readability in the console
print('\n')

# Initialize Pinecone with the API key
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index_name = "news"

# Create a PineconeVectorStore from the existing index
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# Create a retriever from the Pinecone vector store to fetch top 3 relevant documents
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

def get_top_articles(query):
    # Retrieve top 3 articles based on the query
    results = retriever.get_relevant_documents(query)
    # Extract the text content from the results
    articles = [result.page_content for result in results]
    return articles

# Set up the chain of operations
chain = (
    {"context": lambda x: "\n\n".join(get_top_articles(x["question"])), "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

def get_response(query):
    try:
        # Invoke the chain with the query and get the response
        response = chain.invoke({"question": query})
        return response
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        raise

if __name__ == "__main__":
    # Get the query from command line arguments or use a default message
    query = sys.argv[1] if len(sys.argv) > 1 else "Say 'Please provide a valid input'"
    # Print the response to the console
    print(get_response(query))
