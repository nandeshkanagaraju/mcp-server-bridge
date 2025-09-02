from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.mcp.tools.execute_query import execute_query


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
    valid, msg = True, ""  # You can integrate validate_query later
    if not valid:
        raise HTTPException(status_code=400, detail=msg)
    result = execute_query(request.query, db_config)
    return {"result": result}

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("Starting MCP server on http://localhost:8000")
    uvicorn.run("scripts.start_mcp_server:app", host="0.0.0.0", port=8000, reload=True)

