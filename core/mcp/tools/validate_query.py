from config.logger import logger

def validate_query(query: str):
    """
    Basic validation: check if query is a SELECT statement
    """
    logger.info(f"Validating query: {query}")
    if not query.strip().lower().startswith("select"):
        msg = "Only SELECT queries are allowed."
        logger.warning(f"Query validation failed: {msg}")
        return False, msg
    logger.info("Query validation passed")
    return True, ""
