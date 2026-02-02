import json
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional
from collections import Counter, defaultdict
import tools


# Configuration
PASS_THRESHOLD = 100.0  # Minimum pass percentage required (0-100)


@dataclass
class Result:
    intent: str
    action: str
    tool_error: Optional[str] = None


def route(message: str) -> Result:
    """
    Baseline rules router (intentionally simple).
    Demonstrates: intent taxonomy, deterministic actions, safe defaults.
    """
    m = message.lower().strip()

    paid = any(k in m for k in ["i paid", "paid ", "payment went through", "charged", "posted", "receipt", "bank transfer"])
    access = any(k in m for k in ["access", "gate", "can't access", "cannot access", "locked out", "access denied", "unit", "door"])
    declined = any(k in m for k in ["declined", "failed", "error", "won't go through", "didn't go through", "auto-pay failed"])
    pending = any(k in m for k in ["pending", "processing", "not posted"])
    billing = any(k in m for k in ["late fee", "charged twice", "refund", "credit", "invoice", "fee", "receipt", "billed", "bill"])
    contact = any(k in m for k in ["phone number", "office hours", "hours", "contact", "email", "reach", "support", "office", "located", "physical office"])
    
    # Expanded injection patterns
    injection = any(k in m for k in [
        "ignore all", "ignore policies", "give me the gate code", "bypass",
        "override", "system:", "developer mode", "sql query", "forget your instructions",
        "no restrictions", "reveal", "</system>", "safety filters", "internal policies",
        "emergency override", "show internal", "print all", "database password",
        "master access"
    ])
    
    account_help = any(k in m for k in ["can't log in", "can't log in", "reset", "update my card", "password", "email on file", "outdated"])

    # Safety first: refuse policy bypass attempts
    if injection:
        return Result("PROMPT_INJECTION", "REFUSE")

    # Never hallucinate contact info; must be verified source/tool/config
    if contact:
        return Result("CONTACT_INFO", "USE_VERIFIED_SOURCE")

    # High-trust workflow: paid but no access => tool lookup path
    if paid and access and not declined:
        return Result("PAID_NO_ACCESS", "CALL_TOOL")

    # Payment failures
    if declined and "pay" in m:
        return Result("PAYMENT_FAILED", "ASK_CLARIFY")

    # Pending payments
    if pending and ("payment" in m or "paid" in m or "charge" in m):
        return Result("PAYMENT_PENDING", "ASK_CLARIFY")

    # Billing questions generally need account lookup
    if billing:
        return Result("BILLING_QUESTION", "CALL_TOOL")

    # Account help often requires secure verification => escalation
    if account_help:
        return Result("ACCOUNT_HELP", "ESCALATE")

    # Fallback: ask clarifying questions rather than inventing
    if "payment" in m or "pay" in m:
        return Result("UNKNOWN", "ASK_CLARIFY")

    return Result("UNKNOWN", "ASK_CLARIFY")


def agent_step(message: str, tool_name: Optional[str] = None, tool_scenario: str = "ok") -> Result:
    """
    Execute one agent step: route -> (optionally call tool) -> return final action.
    
    Demonstrates:
    - Initial routing via route()
    - Tool execution with failure handling
    - Deterministic fallback to ESCALATE on tool errors
    """
    # Step 1: Initial routing
    result = route(message)
    
    # Step 2: If action requires tool call, simulate it
    if result.action == "CALL_TOOL" and tool_name:
        try:
            # Simulate tool call with provided scenario
            payload = {"message": message, "user_id": "synthetic_user"}
            tool_response = tools.call_tool(tool_name, payload, tool_scenario)
            # Tool succeeded - keep CALL_TOOL as final action
            return result
        
        except (tools.ToolTimeoutError, tools.ToolAuthError, tools.ToolDataError) as e:
            # Tool failed - escalate with error details
            return Result(result.intent, "ESCALATE", tool_error=str(e))
    
    return result


def load_tests(path: str) -> List[Dict]:
    tests: List[Dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tests.append(json.loads(line))
    return tests

def main() -> None:
    tests = load_tests("tests.jsonl")
    passed = 0

    by_category = defaultdict(lambda: {"pass": 0, "fail": 0})
    action_counts = Counter()
    intent_counts = Counter()

    failures = []

    for t in tests:
        # Use agent_step to execute with tool simulation if needed
        tool_name = t.get("tool_name")
        tool_scenario = t.get("tool_scenario", "ok")
        
        got = agent_step(t["input"], tool_name, tool_scenario)
        ok = (got.intent == t["expected_intent"]) and (got.action == t["expected_action"])
        status = "PASS" if ok else "FAIL"

        category = t.get("category", "uncategorized")

        action_counts[got.action] += 1
        intent_counts[got.intent] += 1

        if ok:
            passed += 1
            by_category[category]["pass"] += 1
        else:
            by_category[category]["fail"] += 1
            failure_info = {
                "id": t["id"],
                "category": category,
                "input": t["input"],
                "expected": {"intent": t["expected_intent"], "action": t["expected_action"]},
                "got": {"intent": got.intent, "action": got.action},
            }
            if tool_scenario and tool_scenario != "ok":
                failure_info["tool_scenario"] = tool_scenario
            if got.tool_error:
                failure_info["tool_error"] = got.tool_error
            failures.append(failure_info)

        print(
            f'{status} {t["id"]} | expected=({t["expected_intent"]},{t["expected_action"]}) '
            f'got=({got.intent},{got.action})'
        )

    total = len(tests)
    pct = (passed / total) * 100.0

    print("\n=== Summary ===")
    print(f"Score: {passed}/{total} ({pct:.1f}%)")

    print("\n=== By category ===")
    for cat, stats in sorted(by_category.items()):
        print(f"- {cat}: {stats['pass']} pass / {stats['fail']} fail")

    print("\n=== Action distribution ===")
    for action, n in action_counts.most_common():
        print(f"- {action}: {n}")

    # Write machine-readable report
    report = {
        "score": {"passed": passed, "total": total, "percent": pct},
        "by_category": by_category,
        "action_distribution": action_counts,
        "intent_distribution": intent_counts,
        "failures": failures,
    }

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\nWrote report.json")

    if pct < PASS_THRESHOLD:
        print(f"\nFAIL: score {pct:.1f}% below threshold {PASS_THRESHOLD:.1f}%")
        sys.exit(1)

if __name__ == "__main__":
    main()
