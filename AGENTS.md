# AGENTS.md

Rules for any AI agent working in this vault.

## Core Rules

- `Raw/Sources/` is read-only source material. Never edit or overwrite files here.
- Write compiled knowledge only into `Wiki/`. No exceptions.
- Every compiled Wiki note must link back to at least one file in `Raw/Sources/` via the `sources` frontmatter field.
- Search `Wiki/catalog.jsonl` before opening any Raw source files. Open Raw files only when the compiled Wiki note is insufficient.
- Do not invent citations. Do not create claims that are not supported by a Raw source.
- Run `build`, `lint`, and `source-lint` checks before every commit.

## Layer Summary

| Layer | Path | Purpose |
|-------|------|---------|
| Raw | `Raw/Sources/` | Original source material — never modified |
| Wiki | `Wiki/` | Compiled, reusable knowledge notes |
| Schema | `Schema/` | Rules, contracts, naming conventions |
| Templates | `_templates/` | Blank note templates |
| Skills | `.agents/skills/` | Agent skill definitions |
| Scripts | `scripts/` | Automation tools |

## Workflow

### Ingest
1. A new file appears in `Raw/Sources/`
2. Search the catalog for related existing Wiki notes
3. Open only the most relevant Wiki notes
4. Create or update focused notes in `Wiki/`
5. Add the Raw source path to the `sources` field of every note it informed
6. Keep `source_count` equal to the number of entries in `sources`
7. Run `build`, `lint`, `source-scan --update --accept-covered`, `source-lint`

### Query
1. Start with `Wiki/index.md`
2. Run `search-catalog --query "topic"` to find relevant notes
3. Open the most relevant Wiki notes
4. Open Raw sources only if the compiled note is insufficient or the user asks for source-level detail
5. Cite both the compiled note and the Raw source when answering

### Before Every Commit
```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```
