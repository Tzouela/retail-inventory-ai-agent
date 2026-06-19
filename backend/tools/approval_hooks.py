from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry


class HeaterApprovalHook(HookProvider):
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(BeforeToolCallEvent, self.request_approval)

    def request_approval(self, event: BeforeToolCallEvent):
        tool_name = event.tool_use["name"]

        # Match both direct (modify_setpoint) and Gateway (heater-mcp___modify_setpoint)
        if not tool_name.endswith("modify_setpoint"):
            return

        temperature = event.tool_use["input"].get("temperature")

        approval = event.interrupt(
            name="heater-approval",
            reason={
                "tool": "modify_setpoint",
                "temperature": temperature,
                "message": f"Set heater to {temperature}°C?",
            },
        )

        if approval.lower() not in ["yes", "approve", "confirmed", "ok"]:
            event.cancel_tool = f"User denied: {approval}"
