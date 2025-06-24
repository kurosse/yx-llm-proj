from loguru import logger

from src.agents.agents import fluency_agent, cultural_agent, diachronic_agent


async def delegate_to_fluency_agent(text: str) -> str:
    """
    Checks fluency of the given English text by delegating to fluency_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to fluency agent for text: {text}")
    fluency_result = await fluency_agent.run(f"Rate the fluency of this text: {text}")
    return fluency_result.output


async def delegate_to_cultural_agent(source_text: str, candidate_translation: str) -> str:
    """
    Checks cultural appropriateness of the given English text by delegating to cultural_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to cultural agent for text pair: {source_text}, {candidate_translation}")
    cultural_result = await cultural_agent.run(f"Rate the cultural appropriateness of this pair: {source_text}, {candidate_translation}")
    return cultural_result.output


async def delegate_to_diachronic_agent(source_text: str, candidate_translation: str) -> str:
    """
    Checks diachronic appropriateness of the given English text by delegating to diachronic_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to diachronic agent for text pair: {source_text}, {candidate_translation}")
    diachronic_result = await diachronic_agent.run(f"Rate the diachronic appropriateness of this pair: {source_text}, {candidate_translation}")
    return diachronic_result.output
