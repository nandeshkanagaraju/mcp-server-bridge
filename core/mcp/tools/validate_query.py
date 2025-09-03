from core.mcp.logging_config import setup_logging

logger = setup_logging("ValidateQuery")

def validate_query(query: str):
    """Basic validation: only SELECT queries are allowed."""
    logger.info(f"Validating query: {query}")
    if not query.strip().lower().startswith("select"):
        logger.warning("Query validation failed - only SELECT allowed")
        return False, "Only SELECT queries are allowed."
    logger.info("Query validation passed")
    return True, ""
