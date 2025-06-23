import os

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings

DEEPSEEK_URL = "https://api.deepseek.com/"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


class ModelSelector:
    """
    A class to select and manage different AI models for various tasks.
    """

    def __init__(self):
        self.models = {
            "deepseek_chat": OpenAIModel("deepseek-chat", provider=OpenAIProvider(base_url=DEEPSEEK_URL, api_key=DEEPSEEK_API_KEY)),
            "deepseek_reasoner": OpenAIModel("deepseek-reasoner", provider=OpenAIProvider(base_url=DEEPSEEK_URL, api_key=DEEPSEEK_API_KEY)),
            "gpt_4o_mini": OpenAIModel("gpt-4o-mini"),
        }

    def get_model(self, model_name: str) -> OpenAIModel:
        return self.models.get(model_name, None)


MODEL_SETTINGS = ModelSettings(temperature=1, logprobs=True, top_logprobs=5)
