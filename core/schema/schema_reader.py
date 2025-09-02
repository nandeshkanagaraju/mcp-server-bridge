from config.database import SessionLocal
from sqlalchemy import text

def read_schema():
    session = SessionLocal()
    db_name = session.bind.url.database
    query = text("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :db
    """)
    rows = session.execute(query, {"db": db_name}).fetchall()

    schema = {}
    for table, col, dtype in rows:
        schema.setdefault(table, []).append({"column": col, "type": dtype})
    return schema
