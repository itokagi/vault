# Skill: llm-wiki-lint

Validate the vault before committing. Catch broken links, missing fields, and bad frontmatter.

## When To Use

Before every commit, or on demand to check vault health.

## Steps

1. Run the full maintenance gate:
   ```bash
   python3 scripts/wiki_tool.py doctor
   python3 scripts/wiki_tool.py build
   python3 scripts/wiki_tool.py lint
   python3 scripts/wiki_tool.py source-lint
   python3 scripts/audit_public.py
   ```
2. Read the output carefully
3. Fix any reported errors before committing
4. Re-run until all checks pass

## Common Failures

| Error | Fix |
|-------|-----|
| `source_count` mismatch | Update `source_count` to match length of `sources` |
| Source path not found | Check the path in `sources` points to a real file |
| Disallowed tag | Change to one of: `topic`, `concept`, `entity`, `project`, `log` |
| Processed with no coverage | Create a Wiki note that references the source |
