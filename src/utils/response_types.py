from pydantic import BaseModel

class AgentResponseType(BaseModel):
    agent_name: str
    response: str
    rating: float

class OverallResponseType(BaseModel):
    source_sentence: str
    agent_responses: list[AgentResponseType]
    