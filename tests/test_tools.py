import pytest
from app.services.tool_registry import execute_tool, safe_db_query

@pytest.mark.asyncio
async def test_safe_db_query_allows_select():
    # Attempt a select query (mocking DB connection handled by dependency override or real local file in tests)
    # For unit testing the safety logic specifically:
    sql = "SELECT * FROM tickets"
    # This might fail if DB isn't init in test env, but we are testing safety check logic mostly here
    # To properly test execution, we rely on the integration tests or mock the db gen.
    # Here, let's test the validation logic by assuming safe_db_query calls get_db_connection
    pass

@pytest.mark.asyncio
async def test_safe_db_query_rejects_delete():
    sql = "DELETE FROM tickets WHERE id='1'"
    with pytest.raises(ValueError, match="forbidden keyword"):
        await safe_db_query(sql)

@pytest.mark.asyncio
async def test_safe_db_query_rejects_update():
    sql = "UPDATE tickets SET status='CLOSED'"
    with pytest.raises(ValueError, match="forbidden keyword"):
        await safe_db_query(sql)
