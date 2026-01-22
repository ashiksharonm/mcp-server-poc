from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.routers import system, tools, agent
from app.dependencies import init_db
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting MCP Server POC...")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down MCP Server POC...")

app = FastAPI(
    title="MCP Server POC",
    description="Agent Tool Gateway POC",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(system.router, tags=["System"])
app.include_router(tools.router, tags=["Tools"])
app.include_router(agent.router, tags=["Agent"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
