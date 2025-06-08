import os
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from loguru import logger
from rich import print

from src.agents.basic_agents import fluency_agent
from src.utils.models import ModelSelector
from src.utils.response_types import OverallResponseType

load_dotenv()

# Keep the same system prompt, instructing the LLM to always call all three tools in sequence.
main_system_prompt = """
You are an orchestrator agent that delegates tasks to specialized agents for evaluating the fluency, grammar, and spelling of English sentences.
Your task is to:
1. Receive a source expression in language A and its candidate translation in English.
2. ALWAYS call delegate_to_fluency_agent with the original expression and collect its rating.

Tools available:
- delegate_to_fluency_agent(expression: str)

Whenever you receive any user message, you must call these three tools in this order and return a combined output, even if a tool fails (in which case return a short error note for that tool).
"""

# Initialize the main agent with OpenAIModel + provider; attach the system prompt.
model = ModelSelector().get_model("deepseek_chat")
settings = ModelSettings(temperature=1.3)
main_agent = Agent(model=model, model_settings=settings, system_prompt=main_system_prompt, output_type=OverallResponseType)


# Register each delegate function as a tool. Each takes RunContext and the expression.
@main_agent.tool_plain
async def delegate_to_fluency_agent(expression: str) -> str:
    """
    Checks fluency of the given English expression by delegating to fluency_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to fluency agent for expression: {expression}")
    result = await fluency_agent.run(f"Rate the fluency of this expression: {expression}", message_history=message_history)
    return result.output


# Run loop: call main_agent.run_sync each time. The model will emit the three tool calls in order.
message_history = []
while True:
    user_input_flag = (
        "[green]Please enter a source expression in language A and its candidate translations in English (or type 'exit' to quit):[/green]"
    )
    print(user_input_flag)
    user_input = input().strip()
    if user_input.lower() in ["exit", "quit"]:
        break

    # Pass the full message history from prior runs so that context is preserved.
    result = main_agent.run_sync(user_input, message_history=message_history)
    message_history = result.all_messages()

    # The agent’s final output already concatenates the three ratings.
    print("\n")
    print(f"{result.output}")
