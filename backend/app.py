import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables BEFORE importing tools 
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import current_time
from tools.inventory_tools import check_low_stock, get_sales_velocity
from sub_agents.inventory_analysis_agent import inventory_analysis_agent
from streaming import parse_agent_events
from utils import get_user_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inventory-agent")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """# Retail Inventory Management Agent

You are the main orchestrator for a retail sneaker store's inventory management system.
You coordinate inventory analysis and present recommendations for human approval.

# Your Workflow
When asked to run a stock check or reorder analysis:
1. Call check_low_stock to get all products below minimum stock levels
2. Call get_sales_velocity to get sales data for the last 60 days
3. Pass BOTH results to inventory_analysis_agent for specialist analysis
4. Present the agent's report clearly to the manager for approval
5. Wait for human approval before taking any further action

# Important Rules
- Always use inventory_analysis_agent for analysis — never analyze stock data yourself
- Never place orders or take action without explicit human approval
- If the analysis agent fails, report the error clearly and suggest retrying
- Always remind the manager that their approval is required before any orders are placed
"""

# Bedrock models - us-east-1 is required for Claude Haiku
model = BedrockModel(
    model_id=os.getenv(
        "AGENT_MODEL_ID", "global.anthropic.claude-haiku-4-5-20251001-v1:0"
    ),
    max_tokens=4000,
    region_name="us-east-1",
)

# Global agent instance (lazy initialization)
agent: Agent | None = None


def get_or_create_agent(session_id: str, user_id: str) -> Agent:
    """Get or create the agent instance."""
    global agent
    if agent is None:
        logger.info("Creating Retail Inventory agent")

        agent = Agent(
            name="Retail Inventory Agent",
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=[current_time, check_low_stock, get_sales_velocity, inventory_analysis_agent],
            callback_handler=None,
            trace_attributes={
                "session.id": session_id,
                "user.id": user_id,
            },
        )
    return agent


class InvocationRequest(BaseModel):
    prompt: Optional[str] = None


@app.get("/ping")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/invocations")
async def invocations(payload: InvocationRequest, request: Request):
    """Main agent invocation endpoint with streaming"""
    session_id = request.headers.get(
        "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id", "unknown"
    )
    user_id = get_user_id(request.headers.get("Authorization", ""))

    logger.info(f"Session: {session_id}, User: {user_id}, Prompt: {payload.prompt}")

    if not payload.prompt:
        return {"error": "No prompt provided"}

    agent = get_or_create_agent(session_id, user_id)
    agent_stream = agent.stream_async(payload.prompt)
    parsed_stream = parse_agent_events(agent_stream)

    return StreamingResponse(parsed_stream, media_type="application/x-ndjson")
