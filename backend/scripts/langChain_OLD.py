import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")

parser = StrOutputParser()

# chain = model | parser
# print(chain.invoke("What MLB team won the World Series during the COVID-19 pandemic?"))

template = """
Answer the question based on the context below. If you can't 
answer the question, reply "Please choose from one of our 6 available news topics!".

Context: {context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model | parser
# print(chain.invoke({
#     "context": "Mary's sister is Susana",
#     "question": "Who is Mary's sister?"
# }))

from langchain_openai.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
embedded_query = embeddings.embed_query("Who is Mary's sister?")

print(f"Embedding length: {len(embedded_query)}")
print(embedded_query[:10])

sentence1 = embeddings.embed_query("Mary's sister is Susana")
sentence2 = embeddings.embed_query("Pedro's mother is a teacher")

from sklearn.metrics.pairwise import cosine_similarity

query_sentence1_similarity = cosine_similarity([embedded_query], [sentence1])[0][0]
query_sentence2_similarity = cosine_similarity([embedded_query], [sentence2])[0][0]

print(query_sentence1_similarity, query_sentence2_similarity)

from langchain_community.vectorstores import DocArrayInMemorySearch

vectorstore1 = DocArrayInMemorySearch.from_texts(
    [
        "Mary's sister is Susana",
        "John and Tommy are brothers",
        "Patricia likes white cars",
        "Pedro's mother is a teacher",
        "Lucia drives an Audi",
        "Mary has two siblings",
    ],
    embedding=embeddings,
)

# can now get a retriever directly from the vector store we created before
retriever1 = vectorstore1.as_retriever()
print(retriever1.invoke("Who is Mary's sister?"))

# will allow us to pass the context and question to the prompt as a map with the keys "context" and "question"
setup = RunnableParallel(context=retriever1, question=RunnablePassthrough())
print(setup.invoke("What color is Patricia's car?"))

# adding setup map to the chain
chain = setup | prompt | model | parser 
print(chain.invoke("What color is Patricia's car?"))

print(chain.invoke("What car does Lucia drive?"))


# trying to get functionality with pinecone


print('\n\n')

from pinecone import Pinecone

# # Initialize Pinecone
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index = pc.Index("news-articles")

from langchain_openai.embeddings import OpenAIEmbeddings

# Initialize Pinecone
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "news-articles"

# Create PineconeVectorStore from the existing index
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# Create a retriever from the Pinecone vector store
retriever = vector_store.as_retriever()

# Set up the chain
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# Invoke the chain with a query
response = chain.invoke("What is some exciting news about climate around the globe?")

print(response)


# # Create a retriever from the Pinecone index
# retriever = pinecone.as_retriever(embedding=embeddings)

# # Set up the chain
# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | model
#     | parser
# )

# # Invoke the chain with a query
# response = chain.invoke("What is some exciting news about climate around the globe?")

# print(response)


# # Generate an embedded vector from a hardcoded prompt
# query = "What is some exciting news about climate around the globe?"
# embedded_query = embeddings.embed_query(query)

# # Query Pinecone to find the top 3 most closely related articles
# results = index.query(
#     namespace="ns1",
#     vector=embedded_query,
#     top_k=3,
#     include_values=True,
#     include_metadata=True
# )

# # Extract the context from the top 3 results
# contexts = [result['metadata']['text'] for result in results['matches']]

# chain = (
#     # {"context":contexts, "questions": RunnablePassthrough()}
#      prompt 
#     | model 
#     | parser 
# )

# # Create the input for the model
# input_data = {
#     "context": contexts,
#     "question": query
# }

# response = chain.invoke(input_data)

# print(response)