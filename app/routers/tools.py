from fastapi import APIRouter, HTTPException
from typing import List, Any
from app.schemas import ToolDefinition, ToolRequest, ToolResponse
from app.services.tool_registry import TOOLS, execute_tool
from app.utils.logger import logger
import time

router = APIRouter()

@router.get("/tools", response_model=List[ToolDefinition])
async def list_tools():
    """Return a list of available tools types."""
    return list(TOOLS.values())

@router.post("/tool/{tool_name}", response_model=ToolResponse)
async def run_tool(tool_name: str, request: ToolRequest):
    """Execute a specific tool."""
    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    start_time = time.time()
    try:
        # Validate args against schema (simplified validation here, Pydantic does rest)
        result = await execute_tool(tool_name, request.arguments)
        duration = time.time() - start_time
        
        logger.info(f"Tool {tool_name} executed in {duration:.4f}s")
        return ToolResponse(result=result, meta={"duration_seconds": duration})
        
    except ValueError as e:
        logger.warning(f"Tool input validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
