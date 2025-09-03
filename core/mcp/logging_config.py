# core/mcp/server.py
import asyncio
import nest_asyncio
from fastmcp import FastMCP
from config.logger import setup_logger
from core.mcp.tools.execute_query import execute_query
from core.mcp.tools.get_schema import get_schema
from core.mcp.tools.list_tables import list_tables
from core.mcp.tools.describe_table import describe_table
from core.mcp.tools.get_table_data import get_table_data
from core.mcp.tools.validate_query import validate_query

logger = setup_logger("MCPServer")

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Jeya@4679",
    "database": "company_db"
}

mcp = FastMCP("mcp-nlp-sql-platform")

def run_execute_query(query: str): return execute_query(query, db_config)
def run_get_schema(): return get_schema(db_config)
def run_list_tables(): return list_tables(get_schema(db_config))
def run_describe_table(table_name: str): return describe_table(table_name, db_config)
def run_get_table_data(table_name: str, limit: int = 10): return get_table_data(table_name, db_config, limit)
def run_validate_query(query: str): return validate_query(query)

mcp.tool(run_execute_query)
mcp.tool(run_get_schema)
mcp.tool(run_list_tables)
mcp.tool(run_describe_table)
mcp.tool(run_get_table_data)
mcp.tool(run_validate_query)

async def main():
    logger.info("🚀 Starting MCP Server with MySQL backend...")
    try:
        await mcp.run()
    except Exception as e:
        logger.error(f"Server crashed: {e}")
    finally:
        logger.info("🛑 MCP Server shutting down...")

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
