import os

from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool
from tavily import TavilyClient
from loguru import logger

from src.agents.prompts.agent_prompts import (
    FLUENCY_AGENT_PROMPT,
    TERM_EXTRACTION_AGENT_PROMPT,
    CULTURAL_AGENT_PROMPT,
    DIACHRONIC_AGENT_PROMPT,
)
from src.utils.models import ModelSelector, MODEL_SETTINGS
from src.agents.response_types import (
    FluencyAgentResponseType,
    CulturalAgentResponseType,
    DiachronicAgentResponseType,
    TermExtractionAgentResponseType,
)


async def tavily_culture_search(culturally_significant_term_from_source: str) -> str:
    """
    Searches for the given term using Tavily search engine.
    Returns: a string with search results or an error note.
    """
    tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    query = f"What does {culturally_significant_term_from_source} mean in English?"
    logger.info(f"Searching: {query}")
    response = tavily_client.search(query=query, max_results=5, include_answer=True)
    try:
        return response["answer"]
    except AttributeError:
        logger.error("No answer found in Tavily response.")


fluency_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=FLUENCY_AGENT_PROMPT,
    output_type=FluencyAgentResponseType,
)

term_extraction_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=TERM_EXTRACTION_AGENT_PROMPT,
    tools=[tavily_culture_search],
    output_type=TermExtractionAgentResponseType,
)

cultural_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=CULTURAL_AGENT_PROMPT,
    output_type=CulturalAgentResponseType,
)

diachronic_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=DIACHRONIC_AGENT_PROMPT,
    tools=[tavily_search_tool(os.getenv("TAVILY_API_KEY"))],
    output_type=DiachronicAgentResponseType,
)
