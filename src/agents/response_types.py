from pydantic import BaseModel


##### Fluency Agent Response Types #####
class FluencyAgentResponseType(BaseModel):
    grammar_reasoning: str
    grammar_rating: str
    spelling_reasoning: str
    spelling_rating: str


##### Term Extraction Agent Response Types #####


class CulturallySignificantTermWithExplanation(BaseModel):
    source_original: str
    source_translated: str
    explanation: str


class TermExtractionAgentResponseType(BaseModel):
    culturally_significant_terms_with_explanations: list[CulturallySignificantTermWithExplanation]


##### Cultural Agent Response Types #####
class CulturallySignficantTermAndClues(BaseModel):
    item_from_candidate_translation: str
    item_from_source_original: str
    surrounding_clues_from_source: list[str]
    surrounding_clues_from_candidate: list[str]
    candidate_translation_evaluation: str
    translated_correctly: bool


class CulturalAgentResponseType(BaseModel):
    cultural_reasoning: str | None
    cultural_items_and_clues: list[CulturallySignficantTermAndClues] | None
    cultural_accuracy_rating: str | None


##### Diachronic Agent Response Types #####
class DiachronicTermAndClues(BaseModel):
    item_from_candidate: str | None
    item_from_source: str | None
    inferred_time_period: int | None
    historical_evidence: str | None
    reasoning: str | None
    translated_correctly: bool | None


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
    # diachronic_agent_response: DiachronicAgentResponseType


class OverallResponseType(BaseModel):
    source_sentence: str
    language_code: str
    candidate_sentence_evaluations: list[CandidateSentenceEvaluation]
    best_candidate_id_and_sentence: str
