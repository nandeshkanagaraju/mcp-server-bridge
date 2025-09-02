from sqlalchemy import text
from core.database.connection_manager import get_session


async def execute_sql(sql: str) -> list[dict]:
    """
    Execute a raw SQL query and return results as list of dicts.
    """
    async with get_session() as session:
        result = await session.execute(text(sql))
        rows = result.mappings().all()
        return [dict(row) for row in rows]


async def fetch_table_rows(table_name: str, limit: int = 10) -> list[dict]:
    """
    Fetch rows from a given table.
    """
    sql = f"SELECT * FROM {table_name} LIMIT {limit}"
    return await execute_sql(sql)
