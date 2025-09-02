import mysql.connector

def describe_table(table_name: str, db_config: dict):
    """
    Returns column details of a table
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name};")
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        return columns
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
