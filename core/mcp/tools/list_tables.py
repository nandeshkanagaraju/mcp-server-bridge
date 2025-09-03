from core.mcp.logging_config import setup_logging

logger = setup_logging("ListTables")

def list_tables(tables: list):
    """Return list of tables from schema."""
    logger.info(f"Listing tables: {tables}")
    return tables
