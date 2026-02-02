# LLM Workflow Eval Pack (Reliability MVP)

This repo demonstrates how I approach conversational reliability:
- define workflow intents + expected actions
- build a small eval set (golden tests)
- run regressions so changes don’t break behavior

## What it includes
- `tests.jsonl`: 10 test prompts with expected routing outcomes
- `eval.py`: a tiny baseline router + evaluator (prints pass/fail)

## Why this matters
In production, prompt/tool changes can create regressions.
A small eval pack helps teams measure behavior instead of guessing.

## Failure modes covered
- Misrouting payment issues (e.g., paid but no access)
- Over-eager escalation vs. minimum clarifying questions
- Hallucinated business-critical facts (contact info must be verified)
- Prompt injection attempts (refuse safely)

## Run
```bash
python eval.py

