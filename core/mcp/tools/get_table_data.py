from config.logger import logger
from services.query_service import get_paginated_table_data

async def run_get_table_data(table_name: str, page: int = 1, page_size: int = 100):
    """
    MCP tool to fetch paginated data from a specific table.

    Args:
        table_name: The name of the table.
        page: The page number to fetch.
        page_size: The number of rows per page.
    """
    logger.info(f"Tool 'get_table_data' called for {table_name} with page={page}, page_size={page_size}")

    # Call the service layer to handle the request
    result = await get_paginated_table_data(
        table_name=table_name,
        page=page,
        page_size=page_size
    )

    if result["status"] == "success":
        logger.info(f"Successfully fetched {len(result['data'])} rows from {table_name} for page {page}")
        # The tool can return the full result dict or just the data
        return result 
    else:
        logger.error(f"Failed to fetch data from {table_name}: {result.get('message')}")
        return result