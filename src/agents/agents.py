import os

from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

from src.agents.prompts.agent_prompts import AgentPrompts
from src.utils.models import ModelSelector

fluency_agent = Agent(ModelSelector().get_model("deepseek_chat"), system_prompt=AgentPrompts.FLUENCY_AGENT_PROMPT)
cultural_agent = Agent(
    ModelSelector().get_model("deepseek_chat"),
    system_prompt=AgentPrompts.CULTURAL_AGENT_PROMPT,
    tools=[tavily_search_tool(os.getenv("TAVILY_API_KEY"))],
)


# grammar_agent = Agent(OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY"))), system_prompt=grammar_prompt)
# spelling_agent = Agent(OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY"))), system_prompt=spelling_prompt)
