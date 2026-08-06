from config.logger import logger
from .common_config import db_config
from .execute_query import execute_raw_query

def run_get_schema():
    logger.info("Fetching database schema...")
    query = "SHOW TABLES;"
    result = execute_raw_query(query)
    if result["status"] == "success":
        tables = [list(row.values())[0] for row in result["data"]]
        logger.info(f"Schema fetched: {tables}")
        return tables
    else:
        logger.error("Failed to fetch schema")
        return []
