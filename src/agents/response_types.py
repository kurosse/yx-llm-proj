from pydantic import BaseModel


class FluencyAgentResponseType(BaseModel):
    agent_name: str
    grammar_reasoning: str
    grammar_rating: float
    spelling_reasoning: str
    spelling_rating: float
    translation_candidate: str


##### Cultural Agent Response Types #####
class CulturalClue(BaseModel):
    phrase_or_word: str
    explanation: str


class CulturalItemAndClue(BaseModel):
    item_from_candidate_translation: str
    clue: list[CulturalClue]
    identified_correctly: bool


class CulturalAgentResponseType(BaseModel):
    agent_name: str
    cultural_reasoning: str
    tavily_search: str
    cultural_items_and_clues: list[CulturalItemAndClue]
    cultural_rating: float


##### Orchestrator Response Types #####
class CandidateSentenceEvaluation(BaseModel):
    candidate_sentence: str
    fluency_agent_response: FluencyAgentResponseType
    cultural_agent_response: CulturalAgentResponseType


class OverallResponseType(BaseModel):
    source_sentence: str
    candidate_sentence_evaluations: list[CandidateSentenceEvaluation]
    best_candidate: str
