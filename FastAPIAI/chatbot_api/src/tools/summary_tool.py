from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)
def get_summarize(product_name: str):
    # Khởi tạo client Neo4j
    graph.refresh_schema()

    # Truy vấn Cypher với tên sản phẩm là tham số
    query = """
    MATCH (p:Product)
    WHERE p.name CONTAINS $product_name
    OPTIONAL MATCH (p)<-[:REVIEWED]-(r:Review)
    WITH p, r
    WITH p, collect({content: r.content, rating: r.rating})[0..10] AS topReviews
    RETURN p.specifications AS specifications, p.link AS link, topReviews
    """
    
    # Chạy truy vấn và lấy kết quả
    parameters = {"product_name": product_name}
    results = graph.query(query, parameters)
    
    # Đóng kết nối    
    print(results)
    return results

# get_summarize("Chuột Không Dây Logitech M325 - Hàng Chính Hãng")

