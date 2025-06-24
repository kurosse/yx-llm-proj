from pydantic import BaseModel


##### Fluency Agent Response Types #####
class FluencyAgentResponseType(BaseModel):
    grammar_reasoning: str
    grammar_rating: str
    spelling_reasoning: str
    spelling_rating: str


##### Cultural Agent Response Types #####
class CulturallySignficantTermAndClues(BaseModel):
    item_from_candidate: str
    item_from_source: str
    surrounding_clues_from_source: list[str]
    surrounding_clues_from_candidate: list[str]
    reasoning: str
    translated_correctly: bool


class CulturalAgentResponseType(BaseModel):
    cultural_reasoning: str
    cultural_items_and_clues: list[CulturallySignficantTermAndClues]
    cultural_accuracy_rating: str


##### Diachronic Agent Response Types #####
class DiachronicTermAndClues(BaseModel):
    item_from_candidate: str
    item_from_source: str
    historical_evidence: str
    reasoning: str
    translated_correctly: bool


class DiachronicAgentResponseType(BaseModel):
    diachronic_reasoning: str
    diachronic_terms_and_clues: list[DiachronicTermAndClues]
    diachronic_fidelity_rating: str


##### Orchestrator Response Types #####
class CandidateSentenceEvaluation(BaseModel):
    candidate_sentence: str
    candidate_id: str
    fluency_agent_response: FluencyAgentResponseType
    cultural_agent_response: CulturalAgentResponseType
    diachronic_agent_response: DiachronicAgentResponseType


class OverallResponseType(BaseModel):
    source_sentence: str
    language_code: str
    candidate_sentence_evaluations: list[CandidateSentenceEvaluation]
    best_candidate_id_and_sentence: str
