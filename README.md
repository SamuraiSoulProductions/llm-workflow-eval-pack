# LLM Workflow Eval Pack (Reliability MVP)

This repo demonstrates my approach to **conversational reliability**:
- define workflow intents + expected actions
- build a small eval set (“golden tests”)
- run regressions so changes don’t break behavior

This is the core discipline behind shipping assistants that **complete workflows** and **don’t hallucinate business-critical info**.

---

## What it includes
- `tests.jsonl` — 10 synthetic test prompts with expected routing outcomes  
- `eval.py` — baseline router + evaluator (prints pass/fail)

---

## Why this matters
In production, prompt/tool changes can create regressions:
- misrouted intents (higher escalations)
- missing context (more retries)
- hallucinated contact info/policies (trust damage)

An eval pack makes behavior **measurable** instead of “vibes-based.”

---

## Failure modes covered
- **Paid but no access** → tool lookup path (high-trust workflow)
- **Payment failed / pending** → minimal clarifying questions
- **Contact info** → **must be verified source** (no hallucinations)
- **Prompt injection attempt** → safe refusal + redirect

---

## Run
```bash
python eval.py
