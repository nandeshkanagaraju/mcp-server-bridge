from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from config.logger import logger
from core.mcp.tools.natural_language_query import run_natural_language_query

# Create a new router. We can add a prefix for versioning.
router = APIRouter(prefix="/api/v1")

# Define the request model using Pydantic for automatic validation.
class NLQRequest(BaseModel):
    question: str = Field(..., description="The natural language question to be converted to SQL.")
    session_id: str = Field(..., description="A unique ID to maintain conversation history.")

@router.post("/query/natural-language")
async def handle_natural_language_query(request: NLQRequest):
    """
    This endpoint accepts a natural language question, converts it to a safe SQL query,
    executes it, and returns the result.
    """
    try:
        logger.info(f"Received API request for NLQ on session: {request.session_id}")
        result = await run_natural_language_query(
            question=request.question,
            session_id=request.session_id
        )
        
        if result.get("status") == "error":
            # If the tool returns a known error, return it with a 400 status code.
            raise HTTPException(status_code=400, detail=result.get("message", "An error occurred."))
            
        return result

    except Exception as e:
        logger.critical(f"An unexpected error occurred in the NLQ API endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")