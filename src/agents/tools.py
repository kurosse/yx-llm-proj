from loguru import logger

from src.agents.agents import (
    fluency_agent,
    cultural_agent,
    diachronic_agent,
    term_extraction_agent,
)


async def delegate_to_fluency_agent(text: str) -> str:
    """
    Checks fluency of the given English text by delegating to fluency_agent.
    Returns: a string rating or an error note.
    """
    logger.info(f"Delegating to fluency agent for text: {text}")
    fluency_result = await fluency_agent.run(f"Rate the fluency of this text: {text}")
    return fluency_result.output


async def delegate_to_term_extraction_agent(source_text: str) -> str:
    """
    Extracts culturally significant terms, leveraging the internet.
    Returns: a string with extracted terms or an error note.
    """
    logger.info(f"Delegating to term extraction agent for: {source_text}")
    extraction_result = await term_extraction_agent.run(
        f"Extract culturally significant terms from this pair: {source_text}"
    )
    return extraction_result.output


async def delegate_to_cultural_agent(
    source_text: str,
    identified_culturally_significant_terms: list[dict[str, str]],
    candidate_translation: str,
) -> str:
    """
    Checks cultural appropriateness of the given English text by delegating to cultural_agent.
    Returns: a string rating or an error note.
    """
    logger.info(
        f"Delegating to cultural agent: {source_text}, {identified_culturally_significant_terms}, {candidate_translation}"
    )
    cultural_result = await cultural_agent.run(
        f"Rate the cultural appropriateness of this pair: {source_text}, {candidate_translation} with these culturally significant terms: {identified_culturally_significant_terms}"
    )
    return cultural_result.output


async def delegate_to_diachronic_agent(
    source_text: str, candidate_translation: str
) -> str:
    """
    Checks diachronic appropriateness of the given English text by delegating to diachronic_agent.
    Returns: a string rating or an error note.
    """
    logger.info(
        f"Delegating to diachronic agent: {source_text}, {candidate_translation}"
    )
    diachronic_result = await diachronic_agent.run(
        f"Rate the diachronic appropriateness of this pair: {source_text}, {candidate_translation}"
    )
    return diachronic_result.output
