import re
from typing import Dict, Any, List
from app.schemas import AgentRunResponse
from app.services.tool_registry import execute_tool
from app.config import settings

# Mock "LLM" logic - heuristic based for consistent testing without API keys
async def mock_agent_run(query: str) -> AgentRunResponse:
    query_lower = query.lower()
    tool_calls = []
    answer = "I couldn't figure out which tool to use."

    # Heuristic 1: Ticket Search
    if "ticket" in query_lower or "search" in query_lower:
        # Extract potential keyword using simple splitting
        # E.g., "search for payment ticket" -> "payment"
        match = re.search(r"search.*for\s+(\w+)", query_lower)
        keyword = match.group(1) if match else "login" # default fallback
        
        args = {"query": keyword}
        result = await execute_tool("ticket_search", args)
        tool_calls.append({"tool": "ticket_search", "args": args, "result": result})
        
        count = len(result)
        answer = f"Found {count} tickets related to '{keyword}'."
            
    # Heuristic 2: KB Lookup
    elif "explain" in query_lower or "what is" in query_lower:
        # Extract topic
        match = re.search(r"(explain|what is)\s+(\w+)", query_lower)
        topic = match.group(2) if match else "mcp"
        
        args = {"topic": topic}
        result = await execute_tool("kb_lookup", args)
        tool_calls.append({"tool": "kb_lookup", "args": args, "result": result})
        
        summary = result.get("summary", "No info")
        answer = f"Here is what I found about {topic}: {summary}"

    # Heuristic 3: DB Query
    elif "query" in query_lower or "select" in query_lower:
        # Extract SQL-like string - VERY naive for demo
        # Assume user says "Run query: SELECT * FROM tickets"
        if "select" in query_lower:
             sql_start = query_lower.find("select")
             sql = query[sql_start:] # Take everything from SELECT onwards
             
             args = {"sql": sql}
             try:
                 result = await execute_tool("db_query", args)
                 tool_calls.append({"tool": "db_query", "args": args, "result": result})
                 answer = f"Query executed successfully. Returned {result.get('row_count')} rows."
             except Exception as e:
                 answer = f"Query failed: {str(e)}"

    return AgentRunResponse(answer=answer, tool_calls=tool_calls)

async def run_agent(query: str) -> AgentRunResponse:
    if settings.MOCK_MODE:
        return await mock_agent_run(query)
    
    # Placeholder for real LLM implementation using OpenAI SDK
    # if settings.OPENAI_API_KEY: ...
    
    return await mock_agent_run(query)
