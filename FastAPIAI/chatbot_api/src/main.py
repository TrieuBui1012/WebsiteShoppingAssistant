from fastapi import FastAPI, HTTPException
from agents.product_rag_agent import product_rag_agent_executor
from models.market_rag_query import MarketQueryInput, MarketQueryOutput
from utils.async_utils import async_retry
from asyncio import TimeoutError,wait_for
import logging
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Lyli",
    description="Endpoints for a market online asisstant system graph RAG chatbot",
)

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@async_retry(max_retries=1, delay=1)
async def invoke_agent_with_retry(input: str, timeout: int = 30):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """
    try:
        # Adding a timeout to ensure the query does not hang indefinitely
        response = await wait_for(product_rag_agent_executor.ainvoke({"query": input}), timeout=timeout)
        return response
    except TimeoutError:
        logger.error(f"Query timed out after {timeout} seconds.")
        raise
    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        raise


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/market-rag-agent", response_model=MarketQueryOutput)
async def ask_market_agent(query: MarketQueryInput) -> MarketQueryOutput:
    try:
        # Call the agent with retry mechanism
        query_response = await invoke_agent_with_retry(query.text)
        
        if query_response is None:
            # Log the failure and return a default response indicating failure
            logger.error("invoke_agent_with_retry returned None after all retry attempts.")
            return MarketQueryOutput(
                success=False,
                intermediate_steps=["No response from the agent."],
                output="Failed to get a response."
            )

        # Ensure 'intermediate_steps' exists in the response
        if "intermediate_steps" not in query_response:
            logger.error("Invalid response structure: 'intermediate_steps' key is missing.")
            query_response["intermediate_steps"] = ["No intermediate steps available."]

        # Process intermediate steps into strings if necessary
        try:
            query_response["intermediate_steps"] = [
                str(step) for step in query_response.get("intermediate_steps", [])
            ]
        except Exception as e:
            logger.error(f"Error processing 'intermediate_steps': {e}")
            query_response["intermediate_steps"] = ["Error processing intermediate steps."]

        # Construct the final response object
        final_response = MarketQueryOutput(
            success=True,
            intermediate_steps=query_response.get("intermediate_steps", []),
            output=query_response.get("output", "No output text provided.")
        )
        print("="*20)
        return final_response

    except Exception as e:
        # Catch unexpected errors, log them, and return a failure response
        logger.error(f"Unexpected error in ask_market_agent: {e}")
        return MarketQueryOutput(
            success=False,
            intermediate_steps=["An unexpected error occurred."],
            output=str(e)
        )
    
@app.post("/market-rag-summarize", response_model=MarketQueryOutput)
async def summarize_product(product_name: str):
    try:
        # Call the agent with retry mechanism
        prompt= "Summarize the product with name:" + product_name
        query_response = await invoke_agent_with_retry(prompt)
        
        if query_response is None:
            # Log the failure and return a default response indicating failure
            logger.error("invoke_agent_with_retry returned None after all retry attempts.")
            return MarketQueryOutput(
                success=False,
                intermediate_steps=["No response from the agent."],
                output="Failed to get a response."
            )
    except Exception as e:
        # Catch unexpected errors, log them, and return a failure response
        logger.error(f"Unexpected error in ask_market_agent: {e}")
        return None
        

