from config.logger import logger
from core.database.query_executor import fetch_paginated_table_rows

async def get_paginated_table_data(table_name: str, page: int = 1, page_size: int = 100) -> dict:
    """
    Handles the business logic for retrieving paginated data from a table.
    
    Args:
        table_name: The name of the table.
        page: The page number to retrieve (1-indexed).
        page_size: The number of items per page.
        
    Returns:
        A dictionary containing the status and fetched data.
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 100
        
    # Calculate the offset for the SQL query
    offset = (page - 1) * page_size
    
    logger.info(f"Fetching paginated data for {table_name}: page={page}, page_size={page_size}")
    
    try:
        rows = await fetch_paginated_table_rows(
            table_name=table_name,
            limit=page_size,
            offset=offset
        )
        
        return {
            "status": "success",
            "page": page,
            "page_size": len(rows),
            "data": rows
        }
    except Exception as e:
        logger.error(f"Service error fetching data from {table_name}: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }