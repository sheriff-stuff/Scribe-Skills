# Count Skill Tokens

The [`/count-skill-tokens`](../.claude/commands/count-skill-tokens.md) slash command reports the input-token count of a SKILL.md (or any text file), measured through the Anthropic API's `count_tokens` endpoint.

## Invocation

```
/count-skill-tokens <path-to-SKILL.md>
```

The command runs [`count-skill-tokens.py`](../.claude/commands/scripts/count-skill-tokens.py) with the supplied path. The script reads the file, sends its contents as a single user message to `messages.count_tokens`, and prints the returned token count.

The argument is quoted before it reaches the shell, so an absolute or relative path is accepted, including a Windows backslash path (e.g. `C:\Users\PC\work\Skills\skills\ticket-ultra-review\SKILL.md`) or a path containing spaces. The script trims surrounding quotes and whitespace and reports a clear error when the path is not a file.

## API key

The script reads its Anthropic API key from `.claude/commands/scripts/.anthropic_api_key` — a single-line file beside the script. The key file is gitignored.
