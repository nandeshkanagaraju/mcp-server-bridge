# core/mcp/server.py
import logging
from fastmcp import FastMCP
from core.mcp.tools.execute_query import execute_query
from core.mcp.tools.get_schema import get_schema
from core.mcp.tools.list_tables import list_tables
from core.mcp.tools.describe_table import describe_table
from core.mcp.tools.get_table_data import get_table_data
from core.mcp.tools.validate_query import validate_query

# -------------------- Logging Setup --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("mcp_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MCPServer")

# -------------------- DB Config --------------------
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Jeya@4679",
    "database": "company_db"
}

# -------------------- MCP Init --------------------
mcp = FastMCP("mcp-nlp-sql-platform")

# ---- Wrappers for tools (must be named, not lambdas) ----
def run_execute_query(query: str):
    return execute_query(query, db_config)

def run_get_schema():
    return get_schema(db_config)

def run_list_tables():
    return list_tables(get_schema(db_config))

def run_describe_table(table_name: str):
    return describe_table(table_name, db_config)

def run_get_table_data(table_name: str, limit: int = 10):
    return get_table_data(table_name, db_config, limit)

def run_validate_query(query: str):
    return validate_query(query)

# ---- Register tools ----
mcp.tool(run_execute_query)
mcp.tool(run_get_schema)
mcp.tool(run_list_tables)
mcp.tool(run_describe_table)
mcp.tool(run_get_table_data)
mcp.tool(run_validate_query)

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    logger.info("🚀 Starting MCP Server with MySQL backend...")
    try:
        mcp.run()   # no asyncio.run() -> avoids RuntimeError
    except Exception as e:
        logger.error(f"Server crashed: {e}")
    finally:
        logger.info("🛑 MCP Server shutting down...")
