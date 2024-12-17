from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables once
load_dotenv()

def get_embedding_function():

    api_key = os.getenv('OPENAI_API_KEY')
    embedding_model_name = os.getenv('OPENAI_EMBEDDING')
    if not api_key or not embedding_model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'HOSPITAL_MODEL_NAME' in environment.")

    # Create and return the embeddings object
    embeddings = OpenAIEmbeddings(
        openai_api_key=api_key,
        model=embedding_model_name
    )
    return embeddings

def get_model_function():
    # Retrieve necessary environment variables

    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('HOSPITAL_AGENT_MODEL')
    if not api_key or not model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'HOSPITAL_MODEL_NAME' in environment.")

    # Create and return the chat model object
    model = ChatOpenAI(
        openai_api_key=api_key,
        model=model_name,
        temperature=0.3,
    )
    return model

def get_qa_model_function():
    # Retrieve necessary environment variables

    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('HOSPITAL_QA_MODEL')
    if not api_key or not model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'HOSPITAL_MODEL_NAME' in environment.")

    # Create and return the chat model object
    model = ChatOpenAI(
        openai_api_key=api_key,
        model=model_name,
        temperature=0.3,
    )
    return model

def get_cypher_model_function():
    # Retrieve necessary environment variables

    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('HOSPITAL_CYPHER_MODEL')
    if not api_key or not model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'HOSPITAL_MODEL_NAME' in environment.")

    # Create and return the chat model object
    model = ChatOpenAI(
        openai_api_key=api_key,
        model=model_name,
        temperature=0,
    )
    return model