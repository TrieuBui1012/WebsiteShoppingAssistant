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

neo4j_vector_index = Neo4jVector.from_existing_graph(
    get_embedding_function(),
    graph=graph,
    index_name="reviewContent",
    node_label="Review",
    text_node_properties=[
        "content",
    ],
    retrieval_query="""
    RETURN
        node.content AS text,
        score,
        {
            productName: node.productName,
            released: node.sellerName,
            source: node.link
        } AS metadata
    """,
    embedding_node_property="embedding",
)
retriever = neo4j_vector_index.as_retriever(search_kwargs={'k': 5})

review_template = """Your job is to use customer reviews to answer questions about their experience
with a product or service. Use the following context to answer questions, 
focusing on details that reflect customer satisfaction, product quality, or service experience. 
Be as detailed as possible, but don't make up any information that's not in the context. 
If you don't know an answer based on the context provided, say you don’t know.
{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=review_template)
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["query"], template="{query}")
)
messages = [review_system_prompt, review_human_prompt]

review_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

print("✅✅ Get semantic review search step")

question_answer_chain = create_stuff_documents_chain(model, review_prompt)
review = create_retrieval_chain(
    retriever,
    question_answer_chain
)

def get_review(input):
    # return review
    return review.invoke({"query": query})
