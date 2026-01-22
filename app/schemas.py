from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    name: str = Field(..., description="The unique name of the tool")
    description: str = Field(..., description="What the tool does")
    input_schema: Dict[str, Any] = Field(..., description="JSON schema for the input arguments")
    output_schema: Dict[str, Any] = Field(..., description="JSON schema for the output")
    version: str = "1.0.0"

class ToolRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the tool to execute")
    arguments: Dict[str, Any] = Field(..., description="Input arguments for the tool")

class ToolResponse(BaseModel):
    result: Any = Field(..., description="The output of the tool execution")
    error: Optional[str] = Field(None, description="Error message if execution failed")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Metadata like execution time")

class AgentRunRequest(BaseModel):
    query: str = Field(..., description="User query to process")

class AgentRunResponse(BaseModel):
    answer: str = Field(..., description="Final answer from the agent")
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list, description="List of tools called during execution")
