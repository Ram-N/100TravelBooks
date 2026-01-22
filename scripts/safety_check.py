#!/usr/bin/env python3
"""
Safety check to prevent accidentally committing private content to git.

Run this before commits to verify no sensitive content is staged.
Can be used as a pre-commit hook or run manually.

Usage:
    python scripts/safety_check.py

Exit codes:
    0 - All checks passed, safe to commit
    1 - Dangerous files detected, commit blocked
"""

import subprocess
import sys
import re
from pathlib import Path

# Patterns to block
BLOCKED_PATTERNS = [
    r'^private/',                           # Anything in private/
    r'\.(epub|mobi|pdf|docx)$',            # Book formats
    r'(manuscript|draft|chapter|writeup)',  # Content keywords in path
]

def get_staged_files():
    """Get list of files staged for commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        print("ERROR: Failed to get staged files. Is this a git repository?")
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: git command not found. Is git installed?")
        sys.exit(1)

def check_file(filepath):
    """Check if a file matches any blocked pattern."""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, filepath, re.IGNORECASE):
            return pattern
    return None

def main():
    print("🔒 Running safety check for git commit...")
    print()

    staged_files = get_staged_files()

    if not staged_files:
        print("✓ No files staged for commit.")
        return 0

    blocked_files = []

    for filepath in staged_files:
        pattern = check_file(filepath)
        if pattern:
            blocked_files.append((filepath, pattern))

    if blocked_files:
        print("❌ COMMIT BLOCKED - Dangerous files detected:")
        print()
        for filepath, pattern in blocked_files:
            print(f"  ⚠️  {filepath}")
            print(f"      Matched pattern: {pattern}")
        print()
        print("These files should NOT be committed to a public repository.")
        print("Please unstage them with: git reset HEAD <file>")
        print()
        return 1
    else:
        print(f"✓ All {len(staged_files)} staged files passed safety checks.")
        print()
        print("Staged files:")
        for filepath in staged_files:
            print(f"  • {filepath}")
        print()
        return 0

if __name__ == "__main__":
    sys.exit(main())
