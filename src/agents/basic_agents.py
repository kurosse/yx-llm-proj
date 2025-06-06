import requests
import os

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

from src.utils.common_prompts import RATING_PROMPT

load_dotenv()

model = OpenAIModel("deepseek-chat", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY")))

fluency_prompt = f"You check the English translation for fluency. {RATING_PROMPT}"
grammar_prompt = f"You check the English translation for grammar. {RATING_PROMPT}"
spelling_prompt = f"You check the English translation for spelling. {RATING_PROMPT}"

# main_agent = Agent(model=model, model_settings=settings)

# fluency_agent = Agent(OpenAIModel("gpt-4o-mini"), system_prompt=fluency_prompt)
# grammar_agent = Agent(OpenAIModel("gpt-4o-mini"), system_prompt=grammar_prompt)
# spelling_agent = Agent(OpenAIModel("gpt-4o-mini"), system_prompt=spelling_prompt)

fluency_agent = Agent(OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY"))), system_prompt=fluency_prompt)
grammar_agent = Agent(OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY"))), system_prompt=grammar_prompt)
spelling_agent = Agent(OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url="https://api.deepseek.com/", api_key=os.getenv("DEEPSEEK_API_KEY"))), system_prompt=spelling_prompt)