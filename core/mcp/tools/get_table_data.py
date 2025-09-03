from config.logger import logger
from .execute_query import run_execute_query

def run_get_table_data(table_name: str, limit: int = 10):
    logger.info(f"Fetching data from {table_name}, limit={limit}")
    query = f"SELECT * FROM {table_name} LIMIT {limit};"
    result = run_execute_query(query)
    if result["status"] == "success":
        logger.info(f"Fetched {len(result['data'])} rows from {table_name}")
    else:
        logger.error(f"Failed to fetch data from {table_name}")
    return result["data"] if result["status"] == "success" else []
