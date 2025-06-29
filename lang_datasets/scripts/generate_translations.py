import asyncio
import os

from googletrans import Translator
from pydantic_ai import Agent
from loguru import logger
from tqdm import tqdm
from dotenv import load_dotenv
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import certifi

from lang_datasets.scripts.constants import LANGUAGES, SELECTED_SENTENCES
from src.utils.models import ModelSelector


class GoogleTranslate:
    def __init__(self):
        os.environ["SSL_CERT_FILE"] = certifi.where()

    # Modified async translation function with a counter
    async def translate_text(self, text, src_lang, idx, total):
        async with Translator() as translator:
            result = await translator.translate(text, src=src_lang, dest="en")
            # print(f"Task {idx+1}/{total}: {result.text}")
            return result.text

    # Async helper to translate a list of texts concurrently with progress tracking
    async def translate_all(self, texts, src_lang):
        total = len(texts)
        tasks = [self.translate_text(text, src_lang, idx, total) for idx, text in enumerate(texts)]
        return await asyncio.gather(*tasks)


class NLLBTranslate:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    def translate_text(self, text: str, src_lang: str, target_lang: str = "eng_Latn"):
        self.tokenizer.src_lang = src_lang
        encoded_inputs = self.tokenizer(text, return_tensors="pt")
        forced_bos_id = self.tokenizer.convert_tokens_to_ids(target_lang)
        generated_ids = self.model.generate(**encoded_inputs, forced_bos_token_id=forced_bos_id, max_length=50, num_beams=5, early_stopping=True)
        nllb_translation = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return nllb_translation

    def translate_all(self, texts: list, src_lang: str, target_lang: str = "eng_Latn"):
        nllb_translations = []
        for text in tqdm(texts):
            nllb_translation = self.translate_text(text, src_lang, target_lang)
            nllb_translations.append(nllb_translation)
        return nllb_translations


class LLMTranslateResponseType(BaseModel):
    translation: str


class LLMTranslate:
    def __init__(self):
        model = ModelSelector().get_model("deepseek_chat")
        self.translator = Agent(
            model,
            system_prompt="""You are a translation agent that translates text from one language to another. 
                             Take note of the cultural contexts when performing translations""",
            output_type=LLMTranslateResponseType,
        )

    def translate_text(self, text: str, src_lang: str, target_lang: str = "eng_Latn"):
        translate_prompt = f"Translate the following text from {src_lang} to {target_lang}: {text}"
        response = self.translator.run_sync(translate_prompt)
        return response.output.translation

    def translate_all(self, texts: list, src_lang: str, target_lang: str = "eng_Latn"):
        llm_translations = []
        for text in tqdm(texts):
            llm_translation = self.translate_text(text, src_lang, target_lang)
            llm_translations.append(llm_translation)
        return llm_translations


if __name__ == "__main__":

    load_dotenv()
    translations_dict = {eng_sentence: {} for eng_sentence in SELECTED_SENTENCES}
    goog_translator = GoogleTranslate()
    nllb_translator = NLLBTranslate()
    llm_translator = LLMTranslate()

    progress_counter = 0

    for flores_code, goog_code in LANGUAGES.items():

        # Progress
        logger.info("#" * 50)
        progress_counter += 1
        logger.info(f"Processing translations for {flores_code}. Progress: {progress_counter}/{len(LANGUAGES)}")

        # Get the flores sample file path
        FLORES_SAMPLE_FILE = f"./datasets/flores200_dataset/sample_original/{flores_code}_sample.txt"

        # Read the sample sentences
        with open(FLORES_SAMPLE_FILE, "r", encoding="utf-8") as file:
            translations = [line.strip() for line in file if line.strip()]

        # ##### Google Translate #####
        logger.info(f"Translating {len(translations)} translations from {flores_code} to English using Google Translate...")
        goog_back_translations = asyncio.run(goog_translator.translate_all(translations, goog_code))
        for english_sentence, translation, back_translation in zip(SELECTED_SENTENCES, translations, goog_back_translations):
            translations_dict[english_sentence][flores_code] = {"original": translation, "goog_back_translation": back_translation}

        ##### NLLB Translate #####
        logger.info(f"Translating {len(translations)} translations from {flores_code} to English using NLLB Translate...")
        nllb_back_translations = nllb_translator.translate_all(translations, src_lang=flores_code)
        for english_sentence, translation, back_translation in zip(SELECTED_SENTENCES, translations, nllb_back_translations):
            translations_dict[english_sentence][flores_code].update({"nllb_back_translation": back_translation})

        ##### DeepSeek or ChatGPT Translate #####
        logger.info(f"Translating {len(translations)} translations from {flores_code} to English using LLM Translate...")
        llm_back_translations = llm_translator.translate_all(translations, src_lang=flores_code)
        for english_sentence, translation, back_translation in zip(SELECTED_SENTENCES, translations, llm_back_translations):
            translations_dict[english_sentence][flores_code].update({"llm_back_translation": back_translation})

    # Save the translations to a JSON file
    OUTPUT_FILE = "./datasets/flores200_dataset/flores_sample_translations.json"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        import json

        json.dump(translations_dict, f, ensure_ascii=False, indent=2)

    logger.info(f"Translations completed and saved to {OUTPUT_FILE}")
