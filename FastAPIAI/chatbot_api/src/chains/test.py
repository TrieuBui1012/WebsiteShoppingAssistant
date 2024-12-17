import os
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from dotenv import load_dotenv
from llm.get_llm_function import get_embedding_function, get_model_function
from llm.graph import graph
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()  # Load variables from .env
HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")
model = get_model_function()
graph.refresh_schema()
neo4j_vector_index = Neo4jVector.from_existing_graph(
    get_embedding_function(),
    graph=graph,
    index_name="productDescription",
    node_label="Product",
    text_node_properties=[
        "description",
    ],
    retrieval_query="""
    RETURN
        {
        description: node.description, 
        link: node.link, 
        prodcut_name: node.name, 
        specifications: node.specifications} AS text,
        score,
        {
            productName: node.name,
            released: node.seller_name,
            source: node.link
        } AS metadata
    """,
    embedding_node_property="description_embedding",
)
retriever = neo4j_vector_index.as_retriever(search_kwargs={'k': 5})

retriever.invoke