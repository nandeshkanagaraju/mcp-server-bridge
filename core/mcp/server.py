# core/mcp/server.py
import nest_asyncio
from fastmcp import FastMCP
from config.logger import logger

from core.mcp.tools.execute_query import run_execute_query
from core.mcp.tools.get_schema import run_get_schema
from core.mcp.tools.list_tables import run_list_tables
from core.mcp.tools.describe_table import run_describe_table
from core.mcp.tools.get_table_data import run_get_table_data
from core.mcp.tools.validate_query import run_validate_query

# Apply nest_asyncio to allow running inside existing loops
nest_asyncio.apply()

# Initialize MCP
mcp = FastMCP("mcp-nlp-sql-platform")

# ---- Register all tools ----
mcp.tool(run_execute_query)
mcp.tool(run_get_schema)
mcp.tool(run_list_tables)
mcp.tool(run_describe_table)
mcp.tool(run_get_table_data)
mcp.tool(run_validate_query)

logger.info("🚀 Starting MCP Server with MySQL backend...")

# ---- Start the server ----
try:
    # Direct call to run() avoids asyncio.run conflicts
    mcp.run()
except Exception as e:
    logger.error(f"Server crashed: {e}")
finally:
    logger.info("🛑 MCP Server shutting down...")
