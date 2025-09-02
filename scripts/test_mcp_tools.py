from core.mcp.tools.execute_query import execute_query
from core.mcp.tools.get_schema import get_schema
from core.mcp.tools.list_tables import list_tables
from core.mcp.tools.describe_table import describe_table
from core.mcp.tools.get_table_data import get_table_data
from core.mcp.tools.validate_query import validate_query

# DB config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Jeya@4679",
    "database": "company_db"
}

# 1. Test get_schema
tables = get_schema(db_config)
print("Tables:", list_tables(tables))

# 2. Test describe_table (first table)
if tables:
    desc = describe_table(tables[0], db_config)
    print(f"Description of {tables[0]}:", desc)

# 3. Test get_table_data (first table)
if tables:
    data = get_table_data(tables[0], db_config)
    print(f"Data from {tables[0]}:", data)

# 4. Test execute_query
query = "SELECT * FROM employees LIMIT 5;"
valid, msg = validate_query(query)
if valid:
    result = execute_query(query, db_config)
    print("Query Result:", result)
else:
    print("Invalid query:", msg)
