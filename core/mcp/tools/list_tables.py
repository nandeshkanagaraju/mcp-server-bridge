from config.logger import logger
from .get_schema import run_get_schema

def run_list_tables():
    tables = run_get_schema()
    logger.info(f"Listing tables: {tables}")
    return tables
