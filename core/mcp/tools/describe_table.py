import mysql.connector
from core.mcp.logging_config import setup_logging

logger = setup_logging("DescribeTable")

def describe_table(table_name: str, db_config: dict):
    """Describe a table structure (columns and types)."""
    logger.info(f"Describing table: {table_name}")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE {table_name};")
        description = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.info(f"Table description fetched for {table_name}")
        return description
    except mysql.connector.Error as e:
        logger.error(f"Database error while describing {table_name}: {e}")
        return []
