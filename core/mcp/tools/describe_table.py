from config.logger import logger
from .execute_query import run_execute_query

def run_describe_table(table_name: str):
    logger.info(f"Describing table: {table_name}")
    query = f"DESCRIBE {table_name};"
    result = run_execute_query(query)
    if result["status"] == "success":
        logger.info(f"Table description fetched for {table_name}")
        return result["data"]
    else:
        logger.error(f"Failed to describe table {table_name}")
        return []
