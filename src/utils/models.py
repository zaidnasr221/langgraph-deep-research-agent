import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv(override=True)  # Load environment variables from .env file


def get_llm() -> ChatOpenAI:
    """
    Create and return the chat model used by the research agent.

    The model is served locally through llama.cpp using an
    OpenAI-compatible API.
    """

    base_url = os.getenv("LLM_BASE_URL")
    model_name = os.getenv("LLM_MODEL")
    api_key = os.getenv("LLM_API_KEY", "local")

    if not base_url:
        raise ValueError("LLM_BASE_URL is not set.")

    if not model_name:
        raise ValueError("LLM_MODEL is not set.")

    return ChatOpenAI(
        base_url=base_url,
        model=model_name,
        api_key=api_key,
        temperature=0,
    )