from dotenv import load_dotenv
load_dotenv()
import json

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from loguru import logger
from rich import print

from src.utils.models import ModelSelector
from src.utils.data_parser import parse_json, append_rating
from src.agents.agents import fluency_agent, cultural_agent
from src.agents.prompts.agent_prompts import AgentPrompts
from src.agents.response_types import OverallResponseType

# Initialize some variables
message_history = []
translation_data = parse_json("datasets/sample_dataset/sample.json")

# Initialize the main agent with OpenAIModel + provider; attach the system prompt.
model = ModelSelector().get_model("deepseek_chat")
settings = ModelSettings(temperature=1.3)
main_agent = Agent(model=model, model_settings=settings, system_prompt=AgentPrompts.MAIN_AGENT_PROMPT, output_type=OverallResponseType)


# Register each delegate function as a tool.
@main_agent.tool_plain
async def delegate_to_fluency_agent(expression: str) -> str:
    """
    Checks fluency of the given English expression by delegating to fluency_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to fluency agent for expression: {expression}")
    result = await fluency_agent.run(f"Rate the fluency of this expression: {expression}", message_history=message_history)
    return result.output


@main_agent.tool_plain
async def delegate_to_cultural_agent(source_expression: str, candidate_expression: str) -> str:
    """
    Checks cultural appropriateness of the given English expression by delegating to cultural_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to cultural agent for expression pair: {source_expression}, {candidate_expression}")
    result = await cultural_agent.run(
        f"Rate the cultural appropriateness of this pair: {source_expression}, {candidate_expression}", message_history=message_history
    )
    return result.output


with open("translations.json", "w", encoding="utf-8") as f:
    json.dump([], f, ensure_ascii=False, indent=2)

for translation_data_item in translation_data:
    src_text = translation_data_item["src_text"]
    translations = translation_data_item["translations"]

    # Prompt
    prompt = "src_text: " + src_text
    for translation_id, translation_text in translations.items():
        prompt += f"\n{translation_id}: {translation_text}"
    prompt += "\n\nPlease evaluate the fluency of the translations."

    # Call the orchestrator agent
    result = main_agent.run_sync(prompt, message_history=message_history)
    message_history = result.all_messages()
    print(f"\n{result.output}\n")

    # Append the result to translations.json
    append_rating(result.output, path="translations.json")

    breakpoint()
    # Clear the message history for the next iteration
    message_history.clear()
    breakpoint()


# For manual running, uncomment the following lines:
# while True:
#     user_input_flag = (
#         "[green]Please enter a source expression in language A and its candidate translations in English (or type 'exit' to quit):[/green]"
#     )
#     print(user_input_flag)
#     user_input = input().strip()
#     if user_input.lower() in ["exit", "quit"]:
#         break

#     # Pass the full message history from prior runs so that context is preserved.
#     result = main_agent.run_sync(user_input, message_history=message_history)
#     message_history = result.all_messages()

#     # The agent’s final output already concatenates the three ratings.
#     print("\n")
#     print(f"{result.output}")
