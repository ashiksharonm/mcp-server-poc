from fastapi import APIRouter
from app.schemas import ToolDefinition

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "mcp-server-poc"}
