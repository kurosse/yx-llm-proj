from pydantic import BaseModel

class FluencyAgentResponseType(BaseModel):
    agent_name: str
    grammar_reasoning: str
    grammar_rating: float
    spelling_reasoning: str
    spelling_rating: float
    translation_candidate: str

class CulturalAgentResponseType(BaseModel):
    agent_name: str
    cultural_reasoning: str
    cultural_rating: float
    translation_candidate: str

class OverallResponseType(BaseModel):
    source_sentence: str
    fluency_agent_responses: list[FluencyAgentResponseType]
    cultural_agent_responses: list[CulturalAgentResponseType]
    best_translation_candidate: str