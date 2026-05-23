# Count Skill Tokens

The [`/count-skill-tokens`](../.claude/commands/count-skill-tokens.md) slash command reports the input-token count of a SKILL.md (or any text file), measured through the Anthropic API's `count_tokens` endpoint.

## Invocation

```
/count-skill-tokens <path-to-SKILL.md>
```

The command runs [`count-skill-tokens.py`](../.claude/commands/scripts/count-skill-tokens.py) with the supplied path. The script reads the file, sends its contents as a single user message to `messages.count_tokens`, and prints the returned token count.

## API key

The script reads its Anthropic API key from `.claude/commands/scripts/.anthropic_api_key` — a single-line file beside the script. The key file is gitignored.
