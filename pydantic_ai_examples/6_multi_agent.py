import requests
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

######### WEATHER AGENT #########


class WeatherResultType(BaseModel):
    temperature: float
    weather_code: int
    fun_fact_about_location: str
    result_language: str


weather_agent = Agent(OpenAIModel("gpt-4o-mini"), system_prompt="Be as concise as possible, reply with one sentence.", output_type=WeatherResultType)


@weather_agent.tool_plain  # With dependency injection, we can access the credentials manager
def get_weather_info(latitude: float, longitude: float) -> str:
    """
    Fetches weather information for the given latitude and longitude.
    """
    print(f"Fetching weather info for lat: {latitude}, lon: {longitude}")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode"
    response = requests.get(url)
    return response.json()


######### MATH AGENT #########

math_agent = Agent(OpenAIModel("gpt-4o-mini"), system_prompt="You are a math genius, you can solve complex equations and ELI5.")


######### MAIN AGENT #########

main_agent = Agent(
    OpenAIModel("gpt-4o-mini"),
    system_prompt="You're a helpful assistant that can delegate tasks to specialized agents. If no specialized agent exists, answer the question yourself.",
)


@main_agent.tool_plain
async def delegate_to_weather_agent(location: str) -> str:
    print(f"Delegating to weather agent for location: {location}")
    result = await weather_agent.run(f"What is the weater in {location}?", message_history=message_history)
    return result.output


@main_agent.tool_plain
async def delegate_to_math_agent(expression: str) -> str:
    print(f"Delegating to math agent for: {expression}")
    result = await weather_agent.run(f"Calculate {expression}", message_history=message_history)
    return result.output


message_history = []
while True:
    current_message = input("You: ")
    if current_message.lower() in ["exit", "quit"]:
        break
    result = main_agent.run_sync(current_message, message_history=message_history)
    message_history = result.new_messages()  # or all_messages() to get all messages including the new one, consumes a lot of tokens
    print(result.output)
