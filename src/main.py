import requests
import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings

from src.agents.basic_agents import fluency_agent, grammar_agent, spelling_agent

load_dotenv()


######### MAIN AGENT #########

main_system_prompt = """
You are an orchestrator agent that delegates tasks to specialized agents for evaluating the fluency, grammar, and spelling of English sentences.
Your task is to:
1. Receive a source expression in language A and its candidate translation in English.
2. Delegate the evaluation of fluency, grammar, and spelling to the respective agents.
3. Collect the results from each agent and return a single response containing the ratings for fluency, grammar, and spelling.
4. Always call the tools and ensure that each agent returns a rating for fluency, grammar, and spelling.

You have three tools available:

1. delegate_to_fluency_agent(expression: str)  
   -> use this to check fluency and return a rating.

2. delegate_to_grammar_agent(expression: str)  
   -> use this to check grammar and return a rating.

3. delegate_to_spelling_agent(expression: str)  
   -> use this to check spelling and return a rating.

Whenever you receive any user-message, you must (in this order):
  1) call delegate_to_fluency_agent with the original expression 
  2) then call delegate_to_grammar_agent 
  3) then call delegate_to_spelling_agent 
and finally concatenate the three outputs into a single reply.

If you can't call a tool (e.g. error), just return a brief sentence explaining the failure.

Always run the tools but in any order, and always ensure that a rating is returned for fluency, grammar, and spelling.
"""

model = OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY")))
settings = ModelSettings(temperature=1.3)

main_agent = Agent(model=model, model_settings=settings)


@main_agent.tool_plain
async def delegate_to_fluency_agent(expression: str) -> str:
    print(f"Delegating to fluency agent for: {expression}")
    result = await fluency_agent.run(f"Check the fluency of {expression} and rate it", message_history=message_history)
    return result.output


@main_agent.tool_plain
async def delegate_to_grammar_agent(expression: str) -> str:
    print(f"Delegating to grammar agent for: {expression}")
    result = await grammar_agent.run(f"Check the grammar of {expression} and rate it", message_history=message_history)
    return result.output


@main_agent.tool_plain
async def delegate_to_spelling_agent(expression: str) -> str:
    print(f"Delegating to spelling agent for: {expression}")
    result = await spelling_agent.run(f"Check the spelling of {expression} and rate it", message_history=message_history)
    return result.output


@main_agent.tool_plain
async def evaluate_everything(expression: str) -> str:

    fluency_out = await delegate_to_fluency_agent(expression)
    grammar_out = await delegate_to_grammar_agent(expression)
    spelling_out = await delegate_to_spelling_agent(expression)

    return "\n".join([f"Fluency check: {fluency_out}", f"Grammar check: {grammar_out}", f"Spelling check: {spelling_out}"])


message_history = []
while True:
    current_message = input("You: ")
    if current_message.lower() in ["exit", "quit"]:
        break
    result = main_agent.run_sync(current_message, message_history=message_history)
    message_history = result.new_messages()  # or all_messages() to get all messages including the new one, consumes a lot of tokens
    print(result.output)
