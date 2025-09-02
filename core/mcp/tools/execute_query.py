# execute_query.py
from fastmcp import FastMCP  # Make sure FastMCP is installed
import mysql.connector

def execute_query(query: str, db_config: dict):
    """
    Executes a SQL query using MySQL and returns results as a list of dictionaries.
    
    Args:
        query (str): SQL query to execute
        db_config (dict): Database configuration dictionary with keys:
                          host, user, password, database
                          
    Returns:
        list[dict]: Query results
    """
    try:
        conn = mysql.connector.connect(
            host=db_config.get("host", "localhost"),
            user=db_config.get("user", "root"),
            password=db_config.get("password", ""),
            database=db_config.get("database", "")
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
