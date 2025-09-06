from fastapi import FastAPI
from api import health
# 1. Import the router from our new query_routes.py file
from api.query_routes import router as query_router

app = FastAPI(title="MCP-NLP-SQL Platform")

# 2. Include both the health router and the new query router
app.include_router(health.router)
app.include_router(query_router)

@app.get("/")
def root():
    return {"message": "MCP Server running with MySQL"}