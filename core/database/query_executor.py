from sqlalchemy import text
from core.database.connection_manager import SessionLocal
from config.logger import logger

async def execute_sql(sql: str, params: dict = None) -> list[dict]:
    """
    Execute a raw SQL query with parameters to prevent SQL injection.
    """
    try:
        async with SessionLocal() as session:
            result = await session.execute(text(sql), params)
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error executing SQL query: {e}")
        return []

async def fetch_paginated_table_rows(table_name: str, limit: int, offset: int) -> list[dict]:
    """
    Fetch a paginated set of rows from a given table safely.
    
    Args:
        table_name: The name of the table to query.
        limit: The maximum number of rows to return.
        offset: The number of rows to skip.
        
    Returns:
        A list of rows as dictionaries.
    """
    # Using named parameters (:limit, :offset) to prevent SQL injection.
    sql = f"SELECT * FROM {table_name} LIMIT :limit OFFSET :offset"
    params = {"limit": limit, "offset": offset}

    logger.info(f"Executing paginated query on {table_name}: LIMIT {limit}, OFFSET {offset}")

    return await execute_sql(sql, params)