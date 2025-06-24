import os

from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

from src.agents.prompts.agent_prompts import FLUENCY_AGENT_PROMPT, CULTURAL_AGENT_PROMPT, DIACHRONIC_AGENT_PROMPT
from src.utils.models import ModelSelector, MODEL_SETTINGS
from src.agents.response_types import FluencyAgentResponseType, CulturalAgentResponseType, DiachronicAgentResponseType

fluency_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=FLUENCY_AGENT_PROMPT,
    output_type=FluencyAgentResponseType,
)

cultural_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=CULTURAL_AGENT_PROMPT,
    tools=[tavily_search_tool(os.getenv("TAVILY_API_KEY"))],
    output_type=CulturalAgentResponseType,
)

diachronic_agent = Agent(
    ModelSelector().get_model("deepseek-chat"),
    model_settings=MODEL_SETTINGS,
    system_prompt=DIACHRONIC_AGENT_PROMPT,
    tools=[tavily_search_tool(os.getenv("TAVILY_API_KEY"))],
    output_type=DiachronicAgentResponseType,
)
