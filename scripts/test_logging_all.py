from config.logger import logger
from core.mcp.tools.execute_query import run_execute_query
from core.mcp.tools.get_schema import run_get_schema
from core.mcp.tools.list_tables import run_list_tables
from core.mcp.tools.describe_table import run_describe_table
from core.mcp.tools.get_table_data import run_get_table_data
from core.mcp.tools.validate_query import run_validate_query

def test_all_tools():
    logger.info("===== Starting All Tools Logging Test =====")
    
    try:
        logger.info("Testing execute_query...")
        result = run_execute_query("SELECT * FROM employees LIMIT 3;")
        logger.info(f"execute_query result: {result}")

        logger.info("Testing get_schema...")
        schema = run_get_schema()
        logger.info(f"get_schema result: {schema}")

        logger.info("Testing list_tables...")
        tables = run_list_tables()
        logger.info(f"list_tables result: {tables}")

        if tables:
            table_name = tables[0]
            logger.info(f"Testing describe_table for '{table_name}'...")
            description = run_describe_table(table_name)
            logger.info(f"describe_table result: {description}")

        if tables:
            table_name = tables[0]
            logger.info(f"Testing get_table_data for '{table_name}'...")
            data = run_get_table_data(table_name, limit=3)
            logger.info(f"get_table_data result: {data}")

        logger.info("Testing validate_query...")
        valid = run_validate_query("SELECT * FROM employees LIMIT 3;")
        logger.info(f"validate_query result: {valid}")

    except Exception as e:
        logger.error(f"Error during tools test: {e}")

    logger.info("===== All Tools Logging Test Finished =====")


if __name__ == "__main__":
    test_all_tools()
