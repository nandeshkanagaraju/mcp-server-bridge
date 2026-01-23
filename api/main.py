from fastapi import FastAPI
from api import health
from api.query_routes import router as query_router

app = FastAPI(title="MCP-NLP-SQL Platform")

app.include_router(health.router)
app.include_router(query_router)

@app.get("/")
def root():
    return {"message": "MCP Server running with MySQL"}