#!/usr/bin/env python3
"""audit_public.py — fail on secrets, private paths, and cache state."""

import sys
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent

BANNED_PATTERNS = [
    (r"-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----", "private key"),
    (r"(?i)(api_key|secret_key|password|token)\s*=\s*['\"][^'\"]{8,}", "possible secret"),
    (r"C:\\Users\\" + r"[^\\]+\\", "machine-local Windows path"),
    ("/hom" + "e/[^/]+/", "machine-local Unix path"),
    ("/Use" + "rs/[^/]+/", "machine-local macOS path"),
]

SKIP_DIRS = {".git", ".obsidian", ".claude", "node_modules"}
SKIP_FILES = {"ruvector.db"}
CHECK_EXTENSIONS = {".md", ".py", ".sh", ".json", ".jsonl", ".txt"}


def check_file(path):
    issues = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return issues
    for pattern, label in BANNED_PATTERNS:
        if re.search(pattern, text):
            issues.append(f"{path.relative_to(VAULT_ROOT)}: {label}")
    return issues


def main():
    issues = []
    for path in VAULT_ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.is_file() and path.suffix in CHECK_EXTENSIONS:
            issues.extend(check_file(path))

    if issues:
        for issue in issues:
            print(f"  FAIL: {issue}")
        print(f"audit: {len(issues)} issue(s) found")
        sys.exit(1)
    print("audit: all checks passed")


if __name__ == "__main__":
    main()
