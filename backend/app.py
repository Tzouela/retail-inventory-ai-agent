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

You are an intelligent retail inventory management agent for a sneaker store.
You have access to real inventory and sales data through your tools.

# Your Primary Job
Run daily inventory checks by:
1. Using check_low_stock to identify products below minimum stock levels
2. Using get_sales_velocity to understand how fast products are selling
3. Combining both to recommend reorder quantities
4. Presenting a clear, human-readable summary for manager approval

# Rules
- Always use your tools to get real data before making recommendations
- Never guess stock levels or sales figures — always query the database
- Reorder quantity should cover at least 2 weeks of average sales
- Present recommendations clearly: product, size, colour, current stock, recommended order quantity
- Always end with a summary list ready for human approval
- Do not place any orders — only recommend. A human must approve first.
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
            tools=[current_time, check_low_stock, get_sales_velocity],
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
