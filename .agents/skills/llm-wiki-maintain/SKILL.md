# Skill: llm-wiki-maintain

Keep the Wiki healthy. Rebuild indexes, fix stale links, and keep the catalog current.

## When To Use

At the start of a session, after bulk edits, or when `doctor` reports issues.

## Steps

1. Run `doctor` to assess current state:
   ```bash
   python3 scripts/wiki_tool.py doctor
   ```
2. Rebuild all indexes and the catalog:
   ```bash
   python3 scripts/wiki_tool.py build
   ```
3. Lint all Wiki notes:
   ```bash
   python3 scripts/wiki_tool.py lint
   ```
4. Update the source manifest:
   ```bash
   python3 scripts/wiki_tool.py source-scan --update --accept-covered
   python3 scripts/wiki_tool.py source-lint
   ```
5. Run the public audit:
   ```bash
   python3 scripts/audit_public.py
   ```
6. Fix any issues found, then commit

## Maintenance Checklist

- [ ] `Wiki/catalog.jsonl` is current
- [ ] `Wiki/index.md` and per-folder indexes exist
- [ ] `Schema/source-manifest.jsonl` covers all Raw sources
- [ ] No Wiki note has a broken source link
- [ ] No source is marked `Processed: true` without Wiki coverage
