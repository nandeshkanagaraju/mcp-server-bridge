import mysql.connector
from core.mcp.logging_config import setup_logging

logger = setup_logging("GetTableData")

def get_table_data(table_name: str, db_config: dict, limit: int = 10):
    """Returns table data up to the specified limit."""
    logger.info(f"Fetching data from {table_name}, limit={limit}")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.info(f"Fetched {len(data)} rows from {table_name}")
        return data
    except mysql.connector.Error as e:
        logger.error(f"Database error while fetching data from {table_name}: {e}")
        return []
