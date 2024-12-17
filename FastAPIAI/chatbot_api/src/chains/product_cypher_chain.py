import os
from langchain_neo4j import GraphCypherQAChain
from langchain.prompts import PromptTemplate


from llm.graph import graph
from llm.get_llm_function import get_embedding_function, get_model_function, get_qa_model_function, get_cypher_model_function


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


graph.refresh_schema()


cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly (e.g. [p:product] instead of [:product]). Do not run any
queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement (e.g. WITH v as visit, c.product_price as product_price)
If you need to divide numbers, make sure to
filter the denominator to be non zero.
Here are the example of the question and result cypher:

Question: Hãy cho tôi thông tin chung của sản phẩm Chuột Có Dây Logitech B100 - Hàng Chính Hãng
Cypher:
'''
MATCH (p:Product)
WHERE p.name CONTAINS "Chuột Có Dây Logitech B100 - Hàng Chính Hãng"
OPTIONAL MATCH (p)<-[:REVIEWED]-(r:Review)
WITH p, r
ORDER BY r.date DESC // Optional: Order reviews, e.g., by date
WITH p, collect({{content: r.content, rating: r.rating}})[0..10] AS topReviews
RETURN p.specifications p.link AS specifications, topReviews
'''

You should clean the "'''" in the cypher before return 
Warning:
- Never return a review node without explicitly returning all of the properties
besides the embedding property
- Make sure to use IS NULL or IS NOT NULL when analyzing missing properties.
- You must never include the
statement "GROUP BY" in your query.
- Make sure to alias all statements that
follow as with statement (e.g. WITH v as visit, c.billing_amount as
billing_amount)
- If you need to divide numbers, make sure to filter the denominator to be non
zero.
- Always limit the number of the MATCH by 5

for example:
cypher
Find product in the usb category:
MATCH (p:Product)-[:BELONG_TO]->(c:Category)
WHERE c.name CONTAINS 'USB'
RETURN p.name AS product_name, p.specifications AS specifications, p.rating_average as rating_average, p.brand_name as brand_name, p.link AS product_link, p.price AS product_price LIMIT 5
The question is:


Example looking product suitale for officer
MATCH (p:Product)-[:BELONG_TO]->(c:Category)
WHERE (c.name CONTAINS 'Office' OR c.name CONTAINS 'Work' OR p.description CONTAINS 'ergonomic' OR p.description CONTAINS 'keyboard' OR p.description CONTAINS 'mouse')
RETURN p.name AS product_name, p.description AS product_description, p.price AS product_price
LIMIT 10
"""


cypher_generation_prompt = PromptTemplate(
    input_variables=["schema"],
    template=cypher_generation_template,
)

qa_generation_template = """You are an assistant that takes the results from
a Neo4j Cypher query and forms a human-readable response. The query results
section contains the results of a Cypher query that was generated based on a
user's natural language question. The provided information is authoritative;
you must always use it to construct your response without doubt or correction
using internal knowledge. Make the answer sound like a response to the question.

The user asked the following question:
{input}

A Cypher query was run a generated these results:
{context}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the query results are not empty, you must use the get_customer_service tool to give the user the information of customer service will help the user problem.
If the question involves a time duration, assume the query results
are in units of days unless otherwise specified.

Never say you don't have the right information if there is data in the
query results. Make sure to show all the relevant query results if you're
asked. You must always assume any provided query results are relevant to
answer the question. Construct your response based solely on the provided
query results.

Helpful Answer:
"""


qa_generation_prompt = PromptTemplate(
    input_variables=["context", "input"], template=qa_generation_template
)

# product_cypher_chain = GraphCypherQAChain.from_llm(
#     cypher_llm=get_cypher_model_function(),
#     qa_llm=get_qa_model_function(),
#     node_properties_to_exclude=["embedding","description_embedding"],
#     graph=graph,
#     verbose=True,
#     cypher_prompt=cypher_generation_prompt,
#     validate_cypher=True,
#     allow_dangerous_requests=True,
#     use_function_response=True,
    
# )
# product_cypher_chain.invoke()

chain = GraphCypherQAChain.from_llm(
    llm=get_model_function(),
    cypher_prompt=cypher_generation_prompt,
    qa_prompt=qa_generation_prompt,
    graph=graph,
    verbose=True,
    use_function_response=True,
    exclude_types=["embedding","description_embedding"],
    allow_dangerous_requests=True,
)

def get_the_cypher_chain(query):
    result = chain.invoke({"query": query})
    print(result)
    return result
