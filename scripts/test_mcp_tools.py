from config.logger import logger
from core.mcp.tools.execute_query import run_execute_query
from core.mcp.tools.get_schema import run_get_schema

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Jeya@4679",
    "database": "company_db"
}

def test_tools():
    logger.info("===== Running MCP Tools Test =====")
    
    schema = run_get_schema(db_config)
    logger.info(f"Schema: {schema}")
    
    result = run_execute_query("SELECT * FROM employees LIMIT 5;", db_config)
    logger.info(f"Query Result: {result}")

    logger.info("===== Test Finished =====")

if __name__ == "__main__":
    test_tools()
