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


async def main():
    async with agent.run_stream("What is the capital of Tokyo and what are some good ways to spend time there??") as result:
        async for message in result.stream_text(delta=True):
            print(message)


asyncio.run(main())
