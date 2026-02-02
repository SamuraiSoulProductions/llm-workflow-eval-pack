# Contributing to LLM Workflow Eval Pack

Thank you for your interest in improving this agent reliability demo. This repo maintains high standards for synthetic data and security hygiene.

## Core Principles

### Synthetic Data Only

This repo is a **demonstration project**. All test data, examples, and documentation must remain fully synthetic:

- ✅ Fictional customer scenarios
- ✅ Synthetic unit numbers (e.g., "Unit 555", "Unit 431B")
- ✅ Fake phone numbers (e.g., "555-0100")
- ✅ Generic business patterns

- ❌ Real customer data or PII
- ❌ Actual API credentials or secrets
- ❌ Real business names or identifiers
- ❌ Production logs or error messages
- ❌ Real phone numbers, even if public

### Banned Terms & Content

The repo explicitly rejects:
- `tradingview` (no specific client references)
- `nda` (no confidential material)
- `client logs` (no real logs)
- `verizon` (no specific business references)

If you reference a business, use a generic placeholder instead.

## Before Opening a PR

Run these commands locally to catch hygiene violations early:

```bash
# 1. Syntax check
python -m compileall -q .

# 2. Security hygiene gate (runs banned term checks, JSON validation, etc.)
python hygiene.py

# 3. Run the eval suite
python eval.py
```

**All three must pass.** If any fail, your PR will be blocked in CI.

## What Hygiene Checks

The `hygiene.py` gate validates:

1. **No banned terms** in any `.py`, `.jsonl`, or `.md` file
2. **tests.jsonl validation**:
   - No URLs (`http://`, `https://`)
   - No email addresses (matches `user@domain.com` pattern)
   - All `category="contact"` tests have `expected_action="USE_VERIFIED_SOURCE"`
   - All `tool_scenario` values are valid: `ok`, `timeout`, `auth_error`, `missing_fields`
3. **eval.py config**: Must have `PASS_THRESHOLD` configured

## Adding Tests

When adding new tests to `tests.jsonl`:

- Use realistic-sounding but **completely fictional** inputs
- Keep categories from: `payments_access`, `payments_status`, `billing`, `contact`, `security`, `account`
- For `contact` tests, **always** set `expected_action` to `USE_VERIFIED_SOURCE`
- If test requires tool simulation, include:
  - `tool_name` (e.g., `check_payment_access`, `lookup_billing`)
  - `tool_scenario` (one of: `ok`, `timeout`, `auth_error`, `missing_fields`)

Example:
```json
{"id":"t31","category":"billing","input":"Why wasn't my refund processed yet?","expected_intent":"BILLING_QUESTION","expected_action":"CALL_TOOL","tool_name":"lookup_billing","tool_scenario":"ok","notes":"Refund status lookup."}
```

## Adding Documentation

When adding `.md` files:
- Document using synthetic examples only
- Avoid real brand names or client references
- Use placeholders like "123 Main St, Anytown ST 12345"
- Focus on methodology, not specific real-world deployments

## Code Standards

- **Standard library only**: No external Python dependencies
- **Readability**: Keep functions short and well-commented
- **Testability**: Changes must pass the full eval suite (30/30 tests)
- **Simplicity**: Main entry point stays `python eval.py`

## Questions?

Open an issue or PR with your proposed changes. Maintainers will review for:
- Synthetic data compliance
- Hygiene gate compliance
- Test coverage (30+ tests should remain at 100% pass rate)
- Documentation clarity

Thank you for contributing to reliable agent engineering practices! 🚀
