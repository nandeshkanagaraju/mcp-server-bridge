# scripts/test_mcp_tools.py
from config.logger import setup_logger
from core.mcp.tools.get_schema import get_schema
from core.mcp.tools.list_tables import list_tables
from core.mcp.tools.describe_table import describe_table
from core.mcp.tools.get_table_data import get_table_data
from core.mcp.tools.validate_query import validate_query
from core.mcp.tools.execute_query import execute_query

logger = setup_logger("TestMCP")

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Jeya@4679",
    "database": "company_db"
}

def run_tests():
    logger.info("===== Running MCP Tools Test =====")

    # Schema
    schema = get_schema(db_config)
    logger.info(f"Schema fetched: {schema}")

    # Tables
    tables = list_tables(schema)
    logger.info(f"Tables: {tables}")

    # Describe
    desc = describe_table(tables[0], db_config)
    logger.info(f"Description of {tables[0]}: {desc}")

    # Data
    data = get_table_data(tables[0], db_config, limit=5)
    logger.info(f"Data from {tables[0]} (limit 5): {data}")

    # Validate
    query = "SELECT * FROM employees LIMIT 5;"
    valid, msg = validate_query(query)
    if valid:
        logger.info("Query validation passed")
    else:
        logger.error(f"Validation failed: {msg}")

    # Execute
    result = execute_query(query, db_config)
    logger.info(f"Query Result: {result}")

    logger.info("===== Test Finished =====")

if __name__ == "__main__":
    run_tests()
