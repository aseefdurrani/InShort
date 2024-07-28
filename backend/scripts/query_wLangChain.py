import os
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


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
parser = StrOutputParser()

template = """
Summarize the following articles in a concise manner, highlighting the main ideas of each:

Context: {context}

Question: {question}

Please provide a summary that addresses the question based on the given articles.
"""

prompt = ChatPromptTemplate.from_template(template)
embeddings = OpenAIEmbeddings()

# query_sentence1_similarity = cosine_similarity([embedded_query], [sentence1])[0][0]
# query_sentence2_similarity = cosine_similarity([embedded_query], [sentence2])[0][0]

# print(query_sentence1_similarity, query_sentence2_similarity)


# trying to get functionality with pinecone


print('\n')


# # Initialize Pinecone
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index = pc.Index("news-articles")


# Initialize Pinecone
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index_name = "news-articles"

# Create PineconeVectorStore from the existing index
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# Create a retriever from the Pinecone vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

def get_top_articles(query):
    # Retrieve top 3 articles
    results = retriever.get_relevant_documents(query)
    
    # Extract the text from the results
    articles = [result.page_content for result in results]
    return articles

# Set up the chain
chain = (
    {"context": lambda x: "\n\n".join(get_top_articles(x["question"])), "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# User query
query = "What is some exciting news about climate around the globe?"

# Invoke the chain with the query
response = chain.invoke({"question": query})

print(response)
