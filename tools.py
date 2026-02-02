"""
Simulated tool/integration layer for eval testing.
Demonstrates deterministic failure scenarios for agent reliability testing.
"""

from typing import Dict, Any
import time


class ToolError(Exception):
    """Base class for tool execution errors."""
    pass


class ToolTimeoutError(ToolError):
    """Simulated timeout during tool execution."""
    pass


class ToolAuthError(ToolError):
    """Simulated authentication/authorization failure."""
    pass


class ToolDataError(ToolError):
    """Simulated missing or invalid data fields."""
    pass


def call_tool(tool_name: str, payload: Dict[str, Any], scenario: str = "ok") -> Dict[str, Any]:
    """
    Simulate a tool call with deterministic outcomes based on scenario.
    
    Args:
        tool_name: Name of the tool to call (e.g., 'check_payment_access', 'lookup_billing')
        payload: Input data for the tool (e.g., {'user_id': '123', 'unit': '555'})
        scenario: Simulation scenario - one of: 'ok', 'timeout', 'auth_error', 'missing_fields'
    
    Returns:
        Dict with synthetic tool output for 'ok' scenario
    
    Raises:
        ToolTimeoutError: When scenario='timeout'
        ToolAuthError: When scenario='auth_error'
        ToolDataError: When scenario='missing_fields'
    """
    
    # Simulate failure scenarios
    if scenario == "timeout":
        raise ToolTimeoutError(f"Tool '{tool_name}' timed out after 5000ms")
    
    elif scenario == "auth_error":
        raise ToolAuthError(f"Tool '{tool_name}' authentication failed: invalid API key")
    
    elif scenario == "missing_fields":
        raise ToolDataError(f"Tool '{tool_name}' missing required field: 'account_id'")
    
    elif scenario != "ok":
        raise ValueError(f"Unknown scenario: {scenario}")
    
    # Simulate successful tool execution with synthetic outputs
    if tool_name == "check_payment_access":
        return {
            "status": "success",
            "payment_verified": True,
            "access_granted": True,
            "unit": payload.get("unit", "unknown"),
            "last_payment_date": "2026-02-01",
            "message": "Payment verified, access should be enabled"
        }
    
    elif tool_name == "lookup_billing":
        return {
            "status": "success",
            "account_id": payload.get("account_id", "synthetic_001"),
            "balance": 0.00,
            "last_charge": {
                "amount": 150.00,
                "date": "2026-01-15",
                "description": "Monthly service fee"
            },
            "message": "Billing details retrieved"
        }
    
    elif tool_name == "get_contact_info":
        return {
            "status": "success",
            "phone": "555-0100",
            "email": "support@example.com",
            "hours": "Mon-Fri 9am-5pm EST",
            "address": "123 Main St, Suite 100, Anytown ST 12345"
        }
    
    else:
        # Generic fallback for unknown tools
        return {
            "status": "success",
            "tool": tool_name,
            "message": f"Tool '{tool_name}' executed successfully (synthetic)"
        }
