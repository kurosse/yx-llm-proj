import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")
if openai.api_key is None:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

SYSTEM_PROMPT = """
You are a “Translation Quality Evaluator.” Your task is:
  1. Given one source sentence (in Language A) and its candidate translation (in Language B), determine whether the translation is high-quality enough to be added to a parallel corpus.

  2. Use these evaluation criteria:
     • Semantic Accuracy: Does the translation faithfully preserve meaning and nuance?
     • Fluency & Naturalness: Is the translation grammatically correct and idiomatic in Language B?
     • Completeness: Are there dropped or added ideas compared to the source?
     • Style & Register: Does the tone match (e.g., formal vs. informal)?
     • Cultural Adequacy (optional): If cultural references appear, are they handled appropriately?

  3. For each pair, output a JSON object with exactly these fields:
    {
      "source":      "<the original source sentence>",
      "translation": "<the candidate translation>",
      "decision":    "accept"  or  "reject",
      "score":       <a number from 0.0 to 1.0 indicating overall quality>,
      "explanation": "<a concise rationale—mention which criteria passed or failed>"
    }

  4. Decision logic:
    • If semantic accuracy is perfect (no meaning shifts) AND fluency is native-level AND no major omissions/additions, then "decision": "accept".
    • Otherwise, "decision": "reject".
    • The "score" should reflect how close it is to a perfect translation (e.g., 0.9+ for nearly perfect, <0.5 for poor).

  5. Always produce valid JSON (no extra text). Only include keys exactly as above.
"""

def evaluate_translation_pair(source: str, translation: str) -> str:
    """
    Sends the source+translation to the OpenAI ChatCompletion endpoint
    and returns the raw JSON string produced by the model.
    """
    user_content = f'Source: "{source}"\nTranslation: "{translation}"'

    response = openai.chat.completions.create(
        model="gpt-4o-mini",       # or another GPT model you have access to
        temperature=0.0,           # deterministic output
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_content}
        ],
    )

    # Extract and return the model’s reply (should be a JSON string)
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # Example 1: a high-quality translation
    src1 = "The patient was discharged after two days."
    tgt1 = "病人兩天后出院了。"
    print("=== Example #1 ===")
    print(evaluate_translation_pair(src1, tgt1))
    print()

    # Example 2: a more nuanced case
    src2 = "Climate change affects agricultural output globally."
    tgt2 = "全球暖化影響農業產出。"
    print("=== Example #2 ===")
    print(evaluate_translation_pair(src2, tgt2))
    print()

    # If you want to batch-process many pairs, you could loop:
    # pairs = [
    #     ("Source sentence A", "Translation A"),
    #     ("Source sentence B", "Translation B"),
    #     # …more pairs…
    # ]
    # for (s, t) in pairs:
    #     json_output = evaluate_translation_pair(s, t)
    #     # parse the JSON or write it to a file, etc.
    #     print(json_output)
