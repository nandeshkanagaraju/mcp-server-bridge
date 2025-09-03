from config.logger import logger
from .common_config import db_config
import mysql.connector

def run_execute_query(query: str):
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
