import mysql.connector
from core.mcp.logging_config import setup_logging

logger = setup_logging("GetSchema")

def get_schema(db_config: dict):
    """Fetch list of tables in the database."""
    logger.info("Fetching schema (list of tables)...")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        logger.info(f"Schema fetched: {tables}")
        return tables
    except mysql.connector.Error as e:
        logger.error(f"Database error while fetching schema: {e}")
        return []
