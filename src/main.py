import json

from dotenv import load_dotenv

load_dotenv()
from pydantic_ai import Agent

from src.utils.models import ModelSelector, MODEL_SETTINGS
from src.utils.data_parser import parse_json, append_rating
from src.agents.prompts.agent_prompts import MAIN_AGENT_PROMPT
from src.agents.response_types import OverallResponseType
from src.agents.tools import delegate_to_fluency_agent, delegate_to_cultural_agent, delegate_to_diachronic_agent

# Constants
RATINGS_FILE = "ratings.json"
DATASET_PATH = "datasets/flores200_dataset/flores_sample_translations.json"

# Initialize some variables
message_history = []
translation_data = parse_json(DATASET_PATH)

# Initialize the main agent with OpenAIModel + provider; attach the system prompt.
model = ModelSelector().get_model("deepseek-chat")
settings = MODEL_SETTINGS

main_agent = Agent(
    model=model,
    model_settings=settings,
    system_prompt=MAIN_AGENT_PROMPT,
    output_type=OverallResponseType,
    tools=[delegate_to_fluency_agent, delegate_to_cultural_agent, delegate_to_diachronic_agent],
)


with open(RATINGS_FILE, "w", encoding="utf-8") as f:
    json.dump([], f, ensure_ascii=False, indent=2)

for original_sentence, translation_contents in translation_data.items():
    for language_code, translations in translation_contents.items():

        src_text = translations["original"]
        translations = {
            "candidate_1": translations["goog_back_translation"],
            "candidate_2": translations["nllb_back_translation"],
            "candidate_3": translations["llm_back_translation"],
        }

        # Prompt
        prompt = f"src_text {language_code}: " + src_text
        for translation_id, translation_text in translations.items():
            prompt += f"\n{translation_id}: {translation_text}"
        prompt += "\n\nPlease evaluate the fluency of the translations."

        # Call the orchestrator agent
        result = main_agent.run_sync(prompt, message_history=message_history)
        message_history = result.all_messages()

        # Append the result to translations.json
        append_rating(result.output, path=RATINGS_FILE)

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
