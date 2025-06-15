from pydantic import BaseModel


class FluencyAgentResponseType(BaseModel):
    grammar_reasoning: str
    grammar_rating: float
    spelling_reasoning: str
    spelling_rating: float


##### Cultural Agent Response Types #####
class CulturalClue(BaseModel):
    phrase_or_word: str
    explanation: str


class CulturalItemAndClue(BaseModel):
    item_from_candidate_translation: str
    clue: list[CulturalClue]
    identified_correctly: bool


class CulturalAgentResponseType(BaseModel):
    cultural_reasoning: str
    tavily_search: str
    cultural_items_and_clues: list[CulturalItemAndClue]
    cultural_rating: float


##### Orchestrator Response Types #####
class CandidateSentenceEvaluation(BaseModel):
    candidate_sentence: str
    candidate_id: str
    fluency_agent_response: FluencyAgentResponseType
    cultural_agent_response: CulturalAgentResponseType


class OverallResponseType(BaseModel):
    source_sentence: str
    language_code: str
    candidate_sentence_evaluations: list[CandidateSentenceEvaluation]
    best_candidate_id_and_sentence: str
