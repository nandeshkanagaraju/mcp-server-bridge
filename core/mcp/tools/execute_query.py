import mysql.connector
from core.mcp.logging_config import setup_logging

logger = setup_logging("ExecuteQuery")

def execute_query(query: str, db_config: dict) -> dict:
    """Executes a SQL query using MySQL and returns results."""
    logger.info(f"Executing query: {query}")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.info(f"Query successful. Returned {len(results)} rows.")
        return {"status": "success", "data": results}

    except mysql.connector.Error as e:
        error_msg = f"Database error: {e}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}
