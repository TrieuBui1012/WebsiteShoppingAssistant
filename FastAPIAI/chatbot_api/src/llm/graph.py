from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Initialize the Neo4jGraph connection using environment variables
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

def get_graph():
    return graph
