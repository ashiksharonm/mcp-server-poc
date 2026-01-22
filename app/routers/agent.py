from fastapi import APIRouter, HTTPException
from app.schemas import AgentRunRequest, AgentRunResponse
from app.services.agent_runner import run_agent

router = APIRouter()

@router.post("/agent/run", response_model=AgentRunResponse)
async def agent_endpoint(request: AgentRunRequest):
    """Run the agent simulation."""
    try:
        response = await run_agent(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
