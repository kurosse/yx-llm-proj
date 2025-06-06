import os
import asyncio

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv()

# agent = Agent('openai:gpt-4o-mini')
oai_agent = Agent(
    OpenAIModel("gpt-4o-mini"), system_prompt="You are a geography expert. Answer questions about geography accurately and concisely."
)  # Use OpenAI GPT-4o Mini
# ds_agent = Agent(
#     OpenAIModel("deepseek-chat", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY")))
# )

agent = oai_agent

message_history = []
while True:
    current_message = input("You: ")
    if current_message.lower() in ["exit", "quit"]:
        break
    result = agent.run_sync(current_message, message_history=message_history)
    message_history = result.new_messages() # or all_messages() to get all messages including the new one, consumes a lot of tokens
    print(result.output)
