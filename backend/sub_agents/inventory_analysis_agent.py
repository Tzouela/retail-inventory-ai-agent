import os
import logging
from typing import AsyncIterator
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from pydantic import BaseModel, Field
from tools.types import SubAgentResult

logger = logging.getLogger(__name__)


class InventoryReportResponse(BaseModel):
    """Structured response from the inventory analysis agent"""
    report: str = Field(
        description="Full markdown reorder recommendation report for human review and approval"
    )
    products_count: int = Field(
        description="Number of distinct products requiring reorder"
    )
    total_units: int = Field(
        description="Total units recommended for reorder across all products"
    )


INVENTORY_ANALYSIS_PROMPT = """# Inventory Analysis Agent

You are a specialist retail inventory analyst. You receive raw inventory data and produce clear, actionable reorder recommendations.

# Your Task
When given low stock data and sales velocity data, you must:

1. **Analyze** which products are below minimum stock levels
2. **Prioritize** by urgency — combine stock criticality with sales velocity:
   - CRITICAL: quantity <= 2 AND high sales velocity
   - HIGH: quantity <= 4 AND moderate sales velocity
   - MEDIUM: quantity < minimum but not urgent
3. **Calculate** reorder quantity for each item:
   - Formula: (avg_weekly_sales * 2) + (minimum_quantity - current_quantity)
   - Round up to nearest whole number
   - Minimum reorder of 3 units per SKU
4. **Format** a clean markdown report structured as:
   - Header with date/time
   - Critical Priority table
   - High Priority table
   - Medium Priority table
   - Summary totals by product
   - Footer: "READY FOR MANAGER APPROVAL"

# Output Rules
- Always produce a complete report even if only one product needs reordering
- Be specific: include product name, brand, size, colour, current stock, recommended order
- Use markdown tables for readability
- Calculate products_count as number of DISTINCT products (not SKUs)
- Calculate total_units as sum of ALL recommended order quantities
"""


@tool
async def inventory_analysis_agent(
    low_stock_data: list,
    sales_velocity_data: list
) -> AsyncIterator:
    """Analyze inventory data and produce a structured reorder recommendation report.

    This specialist agent receives raw stock and sales data, reasons about
    priorities and reorder quantities, and returns a formatted report
    ready for human approval.

    Args:
        low_stock_data: List of stock entries below minimum quantity
        sales_velocity_data: List of products with their sales velocity metrics

    Yields:
        SubAgentResult events, final yield is InventoryReportResponse
    """
    logger.info(
        f"Inventory analysis agent invoked: {len(low_stock_data)} low stock entries, "
        f"{len(sales_velocity_data)} velocity records"
    )

    try:
        model = BedrockModel(
            model_id=os.getenv(
                "AGENT_MODEL_ID", "global.anthropic.claude-haiku-4-5-20251001-v1:0"
            ),
            max_tokens=4000,
            region_name="us-east-1",
        )

        analysis_agent = Agent(
            name="Inventory Analysis Agent",
            model=model,
            system_prompt=INVENTORY_ANALYSIS_PROMPT,
            callback_handler=None,
        )

        prompt = f"""Please analyze this inventory data and produce a reorder recommendation report.

## Low Stock Data ({len(low_stock_data)} entries)
{low_stock_data}

## Sales Velocity Data ({len(sales_velocity_data)} products)
{sales_velocity_data}

Produce the full report following your instructions."""

        result = None

        try:
            async for event in analysis_agent.stream_async(
                prompt,
                structured_output_model=InventoryReportResponse
            ):
                yield SubAgentResult(agent=analysis_agent, event=event)

                if "result" in event:
                    result = event["result"]

        except Exception as stream_error:
            logger.error(f"Error during agent streaming: {stream_error}")
            yield {
                "report": f"Analysis failed during streaming: {str(stream_error)}",
                "products_count": 0,
                "total_units": 0
            }
            return

        try:
            if result:
                if hasattr(result, 'structured_output') and result.structured_output:
                    yield result.structured_output.model_dump()
                else:
                    logger.warning("No structured output received, returning raw result")
                    yield {
                        "report": str(result),
                        "products_count": 0,
                        "total_units": 0
                    }
            else:
                logger.warning("No result received from analysis agent")
                yield {
                    "report": "Analysis completed but no result was returned",
                    "products_count": 0,
                    "total_units": 0
                }
        except Exception as result_error:
            logger.error(f"Error processing analysis result: {result_error}")
            yield {
                "report": f"Error processing results: {str(result_error)}",
                "products_count": 0,
                "total_units": 0
            }

    except Exception as setup_error:
        logger.error(f"Error setting up inventory analysis agent: {setup_error}")
        yield {
            "report": f"Agent setup failed: {str(setup_error)}",
            "products_count": 0,
            "total_units": 0
        }