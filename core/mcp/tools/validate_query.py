from config.logger import logger

def run_validate_query(query: str):
    logger.info(f"Validating query: {query}")
    if query.strip().lower().startswith(("select", "show")):
        logger.info("Query validation passed")
        return True
    else:
        logger.warning("Query validation failed")
        return False
