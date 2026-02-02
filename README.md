# LLM Workflow Eval Pack

A demonstration of **prompt and agent reliability engineering** through automated regression testing and workflow verification.

---

## What This Demonstrates

This project showcases the core discipline behind production-grade conversational AI systems:

- **Workflow Routing**: Intent taxonomy with deterministic action mapping
- **Verified Sources**: Strict policies preventing hallucinated contact info or business data
- **Safe Fallbacks**: Graceful handling of ambiguous inputs via clarifying questions
- **Regression Protection**: Golden test suite that catches prompt/tool changes before they reach users
- **Security Hardening**: Detection and safe handling of prompt injection attempts

In production systems, prompt and tool changes can silently introduce regressions—misrouted intents, hallucinated information, or broken workflows. This eval pack makes behavior **measurable and verifiable** instead of "vibes-based."

---

## How to Run

```bash
python eval.py
```

The script:
- Runs all tests from `tests.jsonl`
- Prints PASS/FAIL for each test case
- Generates a summary with category breakdowns
- Writes `report.json` with machine-readable results
- Exits non-zero if score falls below threshold (configurable in `eval.py`)

---

## Test Coverage

All tests are **fully synthetic** and designed to demonstrate methodology:

- **Payments + Access** (2 tests): High-trust workflows requiring payment verification
- **Payment Status** (3 tests): Declined/pending payment clarification flows
- **Billing** (2 tests): Account data lookups with escalation rules
- **Contact Info** (1 test): Verified source requirement (anti-hallucination)
- **Security** (1 test): Prompt injection detection and refusal
- **Account Help** (1 test): Identity verification escalation path

Categories map to different routing behaviors and business risk profiles.

---

## Business Impact

This type of reliability work directly affects measurable business metrics:

| Metric | How Evals Help |
|--------|----------------|
| **Completion Rate** | Catch regressions where workflows fail to resolve user requests |
| **Escalation Rate** | Verify routing logic sends high-risk cases to human support |
| **CSAT Score** | Prevent hallucinations and ensure accurate, helpful responses |
| **Support Load** | Identify patterns where automation breaks down, causing ticket volume |

By tracking pass rates across categories, teams can see exactly which workflow types are stable vs. fragile.

---

## CI/CD Integration

GitHub Actions automatically runs the eval suite on every push and pull request:

```yaml
- name: Run evals
  run: python eval.py
```

This creates a quality gate: changes that break routing behavior fail CI before merge.

---

## Failure Modes Covered

- **Paid but no access** → tool lookup path (high-trust workflow)
- **Payment failed / pending** → minimal clarifying questions instead of guessing
- **Contact info requests** → **must use verified source** (no hallucinations)
- **Prompt injection attempts** → safe refusal with alternative path
- **Account help** → escalation to human support with proper identity verification

Each failure mode has explicit test coverage to prevent silent degradation.

---

## Files

- `eval.py` — Router implementation + test harness
- `tests.jsonl` — 10 synthetic test cases with category labels
- `report.json` — Machine-readable eval results (generated on each run)
- `.github/workflows/ci.yml` — CI automation

---

## Philosophy

Production conversational AI isn't about "magic"—it's about:
1. Defining clear intent taxonomies
2. Mapping intents to safe, verified actions
3. Testing relentlessly
4. Measuring what matters

This repo demonstrates that discipline in a minimal, runnable form.
