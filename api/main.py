from fastapi import FastAPI
from api import health

app = FastAPI(title="MCP-NLP-SQL Platform")

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "MCP Server running with MySQL"}
