from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.mcp.tools.execute_query import execute_query
from core.mcp.tools.validate_query import is_safe_query

# Database config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Jeya@4679",  # Update your password
    "database": "company_db"
}

# FastAPI app
app = FastAPI(title="Universal MCP Server")

# Request model
class QueryRequest(BaseModel):
    query: str

# Test endpoint
@app.get("/")
def read_root():
    return {"message": "MCP server is running!"}

# Query endpoint
@app.post("/query")
def run_query(request: QueryRequest):
    if not is_safe_query(request.query):
        raise HTTPException(status_code=400, detail="Unsafe query detected")
    result = execute_query(request.query, db_config)
    return {"result": result}

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("Starting MCP server on http://localhost:8000")
    uvicorn.run("scripts.start_mcp_server:app", host="0.0.0.0", port=8000, reload=True)

