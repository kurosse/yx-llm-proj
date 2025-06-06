import requests
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv()

oai_agent = Agent(OpenAIModel("gpt-4o-mini"), system_prompt="Be as concises as possible, reply with one sentence.")
agent = oai_agent

@agent.tool_plain # No need dependency injection here, just a simple function
def get_weather_info(latitude: float, longitude: float) -> str:
    """
    Fetches weather information for the given latitude and longitude.
    """
    print(f"Fetching weather info for lat: {latitude}, lon: {longitude}")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    return response.json()

message_history = []
while True:
    current_message = input("You: ")
    if current_message.lower() in ["exit", "quit"]:
        break
    result = agent.run_sync(current_message, message_history=message_history)
    message_history = result.new_messages()  # or all_messages() to get all messages including the new one, consumes a lot of tokens
    print(result.output)
