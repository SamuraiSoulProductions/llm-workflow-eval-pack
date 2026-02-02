"""
Security hygiene gate for synthetic-only, defensive eval pack.
Fails fast if repo contains NDA/client terms, real PII, or policy violations.
Stdlib only (no external dependencies).
"""

import json
import re
import sys
from pathlib import Path


# --- Configuration ---
BANNED_TERMS = ["tradingview", "nda", "client logs", "verizon"]
VALID_TOOL_SCENARIOS = {"ok", "timeout", "auth_error", "missing_fields"}


def check_banned_terms() -> bool:
    """
    Scan all .py and .jsonl files for banned NDA/client terms.
    Excludes: documentation (*.md), hygiene.py, tools.py, and venv.
    Returns True if clean, False if violations found.
    """
    violations = []
    
    # Files to skip (documentation, tool files)
    skip_files = {"hygiene.py", "tools.py", "SECURITY.md", "DESIGN.md", "CONTRIBUTING.md", "README.md"}
    
    for filepath in Path(".").rglob("*"):
        if not filepath.is_file():
            continue
        
        # Skip excluded files and docs
        if filepath.name in skip_files:
            continue
        
        # Only check Python and JSON files (not markdown docs)
        if filepath.suffix not in [".py", ".jsonl"]:
            continue
        
        # Skip hidden and venv dirs
        if any(part.startswith(".") or part == "__pycache__" for part in filepath.parts):
            continue
        
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore").lower()
            for term in BANNED_TERMS:
                if term in content:
                    violations.append(f"  {filepath}: found banned term '{term}'")
        except Exception as e:
            pass
    
    if violations:
        print("✗ BANNED TERMS found:")
        for v in violations:
            print(v)
        return False
    
    return True


def check_tests_jsonl() -> bool:
    """
    Validate tests.jsonl for:
    - No URLs (http://, https://)
    - No email-like strings
    - Contact tests must have expected_action == 'USE_VERIFIED_SOURCE'
    - tool_scenario values are valid
    Returns True if clean, False if violations found.
    """
    violations = []
    
    # URL pattern
    url_pattern = re.compile(r"https?://")
    # Email pattern (simple: anything@anything.anything)
    email_pattern = re.compile(r"\b[^@\s]+@[^@\s]+\.[^@\s]+\b")
    
    try:
        with open("tests.jsonl", "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                test = json.loads(line)
                test_id = test.get("id", f"line {line_num}")
                
                # Check for URLs
                full_text = json.dumps(test).lower()
                if url_pattern.search(full_text):
                    violations.append(f"  {test_id}: contains URL")
                
                # Check for email addresses
                if email_pattern.search(full_text):
                    violations.append(f"  {test_id}: contains email-like string")
                
                # Contact tests must use verified source
                category = test.get("category", "")
                if category == "contact":
                    expected_action = test.get("expected_action", "")
                    if expected_action != "USE_VERIFIED_SOURCE":
                        violations.append(
                            f"  {test_id}: contact test but expected_action={expected_action} "
                            f"(must be USE_VERIFIED_SOURCE)"
                        )
                
                # Validate tool_scenario if present
                tool_scenario = test.get("tool_scenario")
                if tool_scenario and tool_scenario not in VALID_TOOL_SCENARIOS:
                    violations.append(
                        f"  {test_id}: invalid tool_scenario='{tool_scenario}' "
                        f"(must be one of: {', '.join(sorted(VALID_TOOL_SCENARIOS))})"
                    )
    
    except FileNotFoundError:
        # If tests.jsonl doesn't exist, skip this check
        return True
    except json.JSONDecodeError as e:
        violations.append(f"  tests.jsonl: invalid JSON at line: {e}")
    
    if violations:
        print("✗ tests.jsonl VIOLATIONS:")
        for v in violations:
            print(v)
        return False
    
    return True


def check_eval_py() -> bool:
    """
    Verify eval.py has PASS_THRESHOLD configured (defensive check).
    Returns True if found, False otherwise.
    """
    try:
        with open("eval.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "PASS_THRESHOLD" in content:
                return True
    except FileNotFoundError:
        pass
    
    print("✗ eval.py: missing PASS_THRESHOLD configuration")
    return False


def main() -> int:
    """
    Run all hygiene checks. Exit 0 if all pass, 1 if any fail.
    """
    print("=" * 60)
    print("Security Hygiene Gate")
    print("=" * 60)
    
    checks = [
        ("Banned terms", check_banned_terms),
        ("tests.jsonl validation", check_tests_jsonl),
        ("eval.py config", check_eval_py),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n▶ {name}...", end=" ")
        try:
            if check_func():
                print("✓")
            else:
                print("✗")
                all_passed = False
        except Exception as e:
            print(f"✗ (error: {e})")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("Hygiene PASS")
        print("=" * 60)
        return 0
    else:
        print("Hygiene FAIL")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
