import os
from typing import Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from typing import List, Dict, Any
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
# from src.chains.hospital_review_chain import reviews_vector_chain
from chains.product_cypher_chain import get_the_cypher_chain
from chains.product_review_chain import get_review
from chains.product_description_chain import get_product_by_description
from langchain_community.chat_message_histories import Neo4jChatMessageHistory

from tools.tools import (
    get_customer_service_infor
    
    
)
from tools.summary_tool import get_summarize
# from tools.summary_tool import cypher_summary
from llm.get_llm_function import get_embedding_function, get_model_function
from llm.graph import graph
from langchain_core.runnables.history import RunnableWithMessageHistory



print("call agent step")



@tool
def explore_marketplace_database(query: str) -> str:
    """
    Useful when you can easyli extract then name or specific information about the product in the query
    Here is few example:
    Question: Hãy cho tôi thông tin chung của sản phẩm Chuột Có Dây Logitech B100 - Hàng Chính Hãng
        Cypher:
        '''
        MATCH (p:Product)
        WHERE p.name CONTAINS "Chuột Có Dây Logitech B100 - Hàng Chính Hãng"
        OPTIONAL MATCH (p)<-[:REVIEWED]-(r:Review)
        WITH p, r
        ORDER BY r.date DESC // Optional: Order reviews, e.g., by date
        RETURN p.specifications p.link AS specifications
        '''
    """

    return get_the_cypher_chain(query)

@tool 
def explore_product_description(query: str) -> str:

    """
    Use the entire prompt as input to the tool.
    Useful when you dont have the specific information in the prompt and you want to search that it will have something 
    For example, if the prompt is "help me find decore product work well for people with small spaces?", 
    "Is HDMI can connect compatible with Macbook "

    This tool fetches relevant information from the marketplace database based on the question.
    """

    result = get_product_by_description().invoke(query)
    print(result)
    return result

@tool 
def get_summarize_product(product_name: str) -> str:

    """
    Use this tools for summarize the information of product.
    """

    result = get_summarize(product_name)
    return result



@tool
def get_customer_service() -> str:
    """
    Retrieve contact information for customer service.
    
    Example:
    "How can I contact customer service?"
    """
    return get_customer_service_infor()

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)
agent_tools = [
    explore_marketplace_database,
    get_summarize_product,
    # explore_product_description,
    get_customer_service,

]

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful chatbot designed to answer questions
            about customer experiences, product data, brands, customer
            review statistics, order details, shipping times, and product
            availability for stakeholders in an online marketplace.
            Wait until the tools return the result. If the tool return not empty like: []
            You have to use that context to answer the user.
            If the tools return emmpty []. You should try other tools.
            If you dont have the answer you can provide the user use the another way to descripe the question.
            If you try few times and cannot provide answer to the user. You should give the customer service information through customer_service() tool
            When you provide product to the user try to give link belong to the product. 
            For example: Điện thoại bàn không dây Panasonic KX-TGB110 - Hàng Chính Hãng [Link]
            Always verify the formate before give answer to the user.

            When summarize the product you should take the review of product. Give your opinion about the overview of the product. Dont use bullet point. Write it as the paragraph
            IMPORTANT: The OUTPUT MUST BE IN VIETNAMESE
            """
        ),
        # MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent_llm_with_tools = get_model_function().bind_tools(agent_tools)

product_rag_agent = (
    {
        "query": lambda x: x["query"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        # "chat_history": lambda x: x["chat_history"],
    }
    | agent_prompt
    | agent_llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

product_rag_agent_executor = AgentExecutor(
    agent=product_rag_agent,
    tools=agent_tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

# chat_agent = RunnableWithMessageHistory(
#     product_rag_agent_executor,
#     get_memory,
#     input_messages_key="query",
#     history_messages_key="chat_history",
# )
