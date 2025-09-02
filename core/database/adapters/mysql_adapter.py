from sqlalchemy import text
from config.database import SessionLocal

class MySQLAdapter:
    def __init__(self):
        self.session = SessionLocal()

    def execute(self, query: str):
        with self.session.begin():
            result = self.session.execute(text(query))
            return [dict(row._mapping) for row in result]

    def list_tables(self):
        query = text("SHOW TABLES")
        result = self.session.execute(query)
        return [row[0] for row in result]
