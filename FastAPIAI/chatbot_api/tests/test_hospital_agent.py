import pytest
from src.agents.product_rag_agent import product_rag_agent_executor


@pytest.fixture
def input_examples() -> dict[str, list[str]]:
    """
    Example dictionary to test agent tool calling
    """

    examples = {
        "graph_examples": [
            "List the hospitals in the hospital system.",
            "What is the average billing amount?",
        ],
        "experience_examples": [
            "What are patients saying about hospital organization?",
            "What have patients said about the nursing staff at Wallace-Hamilton?",
        ],
        "wait_time_examples": ["What is the current wait time at Wallace-Hamilton?"],
        "availability_examples": [
            "Which hospital has the shortest wait time right now?"
        ],
    }

    return examples


def test_agent_tool_calling(input_examples: dict[str, list[str]]) -> None:
    """
    Test to ensure the hospital agent calls the correct tools
    """

    for example in input_examples["graph_examples"]:
        response = product_rag_agent_executor.invoke({"input": example})

        assert response["intermediate_steps"][0][0].tool == "explore_hospital_database"

    for example in input_examples["experience_examples"]:
        response = product_rag_agent_executor.invoke({"input": example})

        assert (
            response["intermediate_steps"][0][0].tool == "explore_patient_experiences"
        )

    for example in input_examples["availability_examples"]:
        response = product_rag_agent_executor.invoke({"input": example})

        assert (
            response["intermediate_steps"][0][0].tool == "find_most_available_hospital"
        )
