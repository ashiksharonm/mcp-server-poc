import pytest

@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mcp-server-poc"}

@pytest.mark.asyncio
async def test_list_tools(async_client):
    response = await async_client.get("/tools")
    assert response.status_code == 200
    tools = response.json()
    assert len(tools) >= 3
    tool_names = [t["name"] for t in tools]
    assert "ticket_search" in tool_names
    assert "kb_lookup" in tool_names
    assert "db_query" in tool_names

@pytest.mark.asyncio
async def test_run_agent_ticket_search(async_client):
    # Depending on seed data, this might fail if DB not init. 
    # But lifespan should run on app startup in TestClient if using recent FastAPI/Starlette versions.
    # Otherwise we might need to manually trigger init_db in fixture.
    payload = {"query": "Find tickets regarding login"}
    response = await async_client.post("/agent/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "tickets" in data["answer"] or "Found" in data["answer"]
    assert len(data["tool_calls"]) > 0
    assert data["tool_calls"][0]["tool"] == "ticket_search"
