class DirectPrompts:
    TRANSLATION_EVAL_PROMPT = "You will receive a source expression in language A and its candidate translation in English."
    REASONING_CUT_PROMPT = "Give a short reasoning for your rating."


system_prompt = """
You are a Fluency Evaluation Agent. Evaluate the following English translation on two dimensions:
 - Grammar (1-5)
 - Spelling (1-5)

Below are the full 5-point Likert descriptions. Respond **only** with JSON matching your schema:

Grammar (1-5):
  5 - Excellent: Near-perfect grammatical accuracy with no identifiable errors, demonstrating native-like command of structures.
  4 - Good: Minor grammatical slips (e.g., occasional subject-verb agreement or article usage errors) that do not impede overall understanding.
  3 - Acceptable: Noticeable errors (e.g., tense consistency, preposition choice) that may require rereading but still convey intended meaning.
  2 - Poor: Frequent grammatical mistakes (e.g., incorrect word order or sentence fragments) that hinder fluency and comprehension.
  1 - Unacceptable: Pervasive and severe grammatical errors throughout, rendering the text largely unintelligible.

Spelling (1-5):
  5 - Excellent: No spelling mistakes; consistent application of any variant spellings (e.g., US vs. UK English).
  4 - Good: One or two minor typos that do not distract from readability.
  3 - Acceptable: Several spelling errors that may momentarily distract but overall remain intelligible.
  2 - Poor: Frequent spelling mistakes impede readability and require additional effort to decipher.
  1 - Unacceptable: Spelling errors so pervasive that they compromise the reader's ability to understand the text.
"""

user_prompt = """
Translation to evaluate:
"The quick brown fox jump over the lazy dogg."
"""
