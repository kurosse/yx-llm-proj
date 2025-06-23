from pydantic import BaseModel


##### Fluency Agent Response Types #####
class FluencyAgentResponseType(BaseModel):
    grammar_reasoning: str
    grammar_rating: int
    spelling_reasoning: str
    spelling_rating: int


##### Cultural Agent Response Types #####
class CulturallySignficantTermAndClues(BaseModel):
    item_from_candidate: str
    item_from_source: str
    surrounding_clues_from_source: list[str]
    surrounding_clues_from_candidate: list[str]
    reasoning_with_tavily_search: str
    translated_correctly: bool


class CulturalAgentResponseType(BaseModel):
    cultural_reasoning: str
    cultural_items_and_clues: list[CulturallySignficantTermAndClues]
    cultural_accuracy_rating: int


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
