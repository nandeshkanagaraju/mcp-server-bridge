import importlib
import pkgutil
from fastmcp import FastMCP

# Initialize MCP app
mcp = FastMCP("UniversalMcp")

# Dynamically import all tools from core.mcp.tools
def load_tools(package_name: str):
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)

# Load all tools automatically
load_tools("core.mcp.tools")

if __name__ == "__main__":
    mcp.run()
