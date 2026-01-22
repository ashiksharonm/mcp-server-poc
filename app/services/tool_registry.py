import asyncio
import random
from typing import List, Dict, Any
from app.schemas import ToolDefinition
from app.dependencies import get_db_connection
from app.utils.logger import logger
from tenacity import retry, stop_after_attempt, wait_fixed

# --- Tool Implementations ---

async def simple_ticket_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search tickets by title using simple SQL LIKE matching."""
    db_gen = get_db_connection()
    async for db in db_gen:
        cursor = await db.execute(
            "SELECT * FROM tickets WHERE title LIKE ? LIMIT ?",
            (f"%{query}%", top_k)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    return []

@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1)) # Fast retry for demo
async def kb_lookup(topic: str) -> Dict[str, Any]:
    """Mock knowledge base lookup with simulated flaky failure."""
    
    # Simulate flaky external service
    if random.random() < 0.2:
        logger.warning(f"Simulating kb_lookup failure for {topic}")
        raise RuntimeError("KB Service temporarily unavailable")

    kb_data = {
        "mcp": {
            "topic": "mcp",
            "summary": "Model Context Protocol (MCP) is a standard for connecting AI models to external tools and data.",
            "sources": ["https://mcp.io", "internal-wiki/mcp"]
        },
        "python": {
            "topic": "python",
            "summary": "Python is a high-level, general-purpose programming language.",
            "sources": ["https://python.org"]
        }
    }
    return kb_data.get(topic.lower(), {"topic": topic, "summary": "No information found.", "sources": []})

async def safe_db_query(sql: str) -> Dict[str, Any]:
    """Execute a READ-ONLY SQL query."""
    normalized_sql = sql.strip().upper()
    if not normalized_sql.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
    
    forbidden = ["UPDATE", "DELETE", "DROP", "INSERT", "ALTER", "TRUNCATE"]
    for word in forbidden:
        if word in normalized_sql:
             raise ValueError(f"Query contains forbidden keyword: {word}")

    db_gen = get_db_connection()
    async for db in db_gen:
        try:
            cursor = await db.execute(sql)
            rows = await cursor.fetchall()
            return {"rows": [dict(row) for row in rows], "row_count": len(rows)}
        except Exception as e:
            logger.error(f"SQL Error: {e}")
            raise ValueError(f"Database error: {str(e)}")
    return {"rows": [], "row_count": 0}

# --- Registry ---

TOOLS: Dict[str, ToolDefinition] = {
    "ticket_search": ToolDefinition(
        name="ticket_search",
        description="Search support tickets by keyword.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        },
        output_schema={"type": "array", "items": {"type": "object"}}
    ),
    "kb_lookup": ToolDefinition(
        name="kb_lookup",
        description="Look up information in the knowledge base.",
        input_schema={
            "type": "object",
            "properties": {
                "topic": {"type": "string"}
            },
            "required": ["topic"]
        },
        output_schema={"type": "object"}
    ),
    "db_query": ToolDefinition(
        name="db_query",
        description="Run a safe SQL query against the database.",
        input_schema={
            "type": "object",
            "properties": {
                "sql": {"type": "string"}
            },
            "required": ["sql"]
        },
        output_schema={"type": "object"}
    )
}

async def execute_tool(name: str, args: Dict[str, Any]) -> Any:
    if name == "ticket_search":
        return await simple_ticket_search(**args)
    elif name == "kb_lookup":
        return await kb_lookup(**args)
    elif name == "db_query":
        return await safe_db_query(**args)
    else:
        raise ValueError(f"Tool {name} not found")
