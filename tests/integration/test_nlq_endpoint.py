import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from api.main import app

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def client():
    """Create an async client for making requests to the app."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

async def test_natural_language_query_endpoint(client: AsyncClient, monkeypatch):
    """
    Tests the full end-to-end flow of the /query/natural-language endpoint.
    """
    async def mock_generate_sql(question: str, schema: str, session_id: str):
        assert question == "how many employees are there"
        return "SELECT COUNT(*) as total FROM employees;"

    monkeypatch.setattr(
        "services.llm_service.generate_sql_from_prompt",
        mock_generate_sql
    )
    
    async def mock_execute_sql(sql: str):
        assert sql == "SELECT COUNT(*) as total FROM employees;"
        return [{"total": 150}]
        
    monkeypatch.setattr(
        "core.mcp.tools.natural_language_query.execute_sql",
        mock_execute_sql
    )
    
    # CHANGE THIS from "async def" to just "def"
    def mock_update_history(*args, **kwargs):
        pass # Do nothing
    
    monkeypatch.setattr(
        "services.llm_service.update_conversation_history",
        mock_update_history
    )

    request_data = {
        "question": "how many employees are there",
        "session_id": "integration_test_session_123"
    }

    response = await client.post("/api/v1/query/natural-language", json=request_data)

    assert response.status_code == 200
    
    response_json = response.json()
    assert response_json["status"] == "success"
    assert response_json["generated_sql"] == "SELECT COUNT(*) as total FROM employees;"
    assert response_json["data"] == [{"total": 150}]