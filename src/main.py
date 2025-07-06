import json
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
from pydantic_ai import Agent
from tqdm import tqdm
from loguru import logger

from src.utils.models import ModelSelector, MODEL_SETTINGS
from src.utils.data_parser import parse_json, append_rating
from src.agents.prompts.agent_prompts import MAIN_AGENT_PROMPT
from src.agents.response_types import OverallResponseType
from src.agents.tools import (
    delegate_to_fluency_agent,
    delegate_to_term_extraction_agent,
    delegate_to_cultural_agent,
    delegate_to_diachronic_agent,
)


# Constants
DATASET_PATH = "lang_datasets/sample_dataset/flores_sample_translations.json"
DATASET_TYPE = "flores200"
RATINGS_FILE = "ratings/flores200-ratings.json"
REMAKE_RATINGS = False

# Create a log file from loguru
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = Path(f"logs/flores200_ratings_{current_time}.log")
log_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
logger.add(log_file_path, rotation="25 MB")

def main():
    # Initialize some variablesF
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
        tools=[
            delegate_to_fluency_agent,
            delegate_to_term_extraction_agent,
            delegate_to_cultural_agent,
            # delegate_to_diachronic_agent,
        ],
    )

    present_source_sentences = []

    # Whether to discard the existing ratings or not, remake if settings are changed.
    if REMAKE_RATINGS:
        with open(RATINGS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    else:
        current_ratings = parse_json(RATINGS_FILE)
        present_source_sentences = [item["source_sentence"] for item in current_ratings]

    for original_sentence, translation_contents in tqdm(translation_data.items()):
        for language_code, translations in translation_contents.items():
            src_text = translations["original"]

            if src_text in present_source_sentences:
                logger.info(f"Skipping already rated source text: {src_text}")
                continue

            translations = {
                "candidate_1": translations["goog_back_translation"],
                "candidate_2": translations["nllb_back_translation"],
                "candidate_3": translations["llm_back_translation"],
            }

            # Prompt
            prompt = f"src_text {language_code}: " + src_text
            for translation_id, translation_text in translations.items():
                prompt += f"\n{translation_id}: {translation_text}"
            prompt += "\n\nPlease evaluate the translations against the src_text."

            # Call the orchestrator agent
            result = main_agent.run_sync(prompt, message_history=message_history)
            message_history = result.all_messages()

            # Append the result to translations.json
            append_rating(
                result.output,
                original_english_text=original_sentence,
                path=RATINGS_FILE,
            )

            # Clear the message history for the next iteration
            message_history.clear()


if __name__ == "__main__":
    main()
