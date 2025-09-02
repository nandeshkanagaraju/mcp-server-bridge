import mysql.connector

def get_table_data(table_name: str, db_config: dict, limit: int = 10):
    """
    Returns table data up to the specified limit
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
