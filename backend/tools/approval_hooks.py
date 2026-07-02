import logging
from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry

logger = logging.getLogger(__name__)


class ReorderApprovalHook(HookProvider):
    """Hook that intercepts place_order tool calls and requires human approval."""

    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(BeforeToolCallEvent, self.request_approval)

    def request_approval(self, event: BeforeToolCallEvent):
        """Intercept place_order calls and request human approval."""
        tool_name = event.tool_use.get("name", "")

        if tool_name != "place_order":
            return

        tool_input = event.tool_use.get("input", {})
        stock_id = tool_input.get("stock_id")
        quantity = tool_input.get("quantity")
        approved_by = tool_input.get("approved_by", "unknown")

        logger.info(f"Intercepting place_order: stock_id={stock_id}, quantity={quantity}")

        approval = event.interrupt(
            name="reorder-approval",
            reason={
                "tool": "place_order",
                "stock_id": stock_id,
                "quantity": quantity,
                "approved_by": approved_by,
                "message": f"Place order for {quantity} units of stock item {stock_id}?",
            },
        )

        if approval.lower() not in ["yes", "approve", "approved", "ok", "confirm"]:
            event.cancel_tool = f"Order cancelled by manager: {approval}"
            logger.info(f"Order cancelled: {approval}")
        else:
            logger.info(f"Order approved by {approved_by}")
