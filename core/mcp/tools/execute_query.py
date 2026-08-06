from config.logger import logger
from core.security.query_validator import is_select_only
from .common_config import db_config
import mysql.connector


def execute_raw_query(query: str):
    """
    Execute a query without validation.

    Internal use only. Callers must pass a query they construct themselves,
    never one supplied by a client. Client input goes through run_execute_query.
    """
    try:
        logger.info(f"Executing query: {query}")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"Query successful. Returned {len(results)} rows.")
        return {"status": "success", "data": results}
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return {"status": "error", "message": str(e)}


def run_execute_query(query: str):
    """
    MCP tool to execute a client-supplied query.

    The query must parse to a single SELECT statement; anything else is
    rejected before it reaches the database.
    """
    if not is_select_only(query):
        logger.warning(f"Rejected query from MCP client: {query}")
        return {
            "status": "error",
            "message": "Rejected: only a single SELECT statement is permitted.",
        }

    return execute_raw_query(query)
