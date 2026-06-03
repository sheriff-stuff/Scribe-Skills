#!/usr/bin/env python
"""Count tokens for a SKILL.md (or any text file) via the Anthropic API."""
import sys
from pathlib import Path
import anthropic

# Require a file path argument. Trim surrounding whitespace and quotes so a
# quoted path (including a Windows backslash path) resolves cleanly.
if len(sys.argv) < 2:
    print("usage: count-skill-tokens.py <path-to-SKILL.md>", file=sys.stderr)
    sys.exit(1)
target = Path(sys.argv[1].strip().strip('"').strip("'"))
if not target.is_file():
    print(f"error: no such file: {target}", file=sys.stderr)
    sys.exit(1)

# Read the API key from a gitignored file next to this script,
# so the key never has to live in the shell environment.
key_file = Path(__file__).with_name(".anthropic_api_key")
if not key_file.exists():
    print(f"error: missing API key file at {key_file}", file=sys.stderr)
    sys.exit(1)
api_key = key_file.read_text(encoding="utf-8").strip()

# Load the target file's contents as a single user message.
with open(target, encoding="utf-8") as f:
    content = f.read()

# Ask the API how many input tokens that content would consume.
response = anthropic.Anthropic(api_key=api_key).messages.count_tokens(
    model="claude-opus-4-7",
    messages=[{"role": "user", "content": content}],
)

print(response.input_tokens)
