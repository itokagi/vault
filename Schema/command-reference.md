# Command Reference

All commands run from the vault root.

## wiki_tool.py

| Command | What it does |
|---------|-------------|
| `python3 scripts/wiki_tool.py doctor` | Health check — folders, Python version, note counts. Non-mutating. |
| `python3 scripts/wiki_tool.py build` | Rebuild `Wiki/catalog.jsonl`, `Wiki/index.md`, and per-folder indexes. |
| `python3 scripts/wiki_tool.py lint` | Validate all compiled Wiki note frontmatter, tags, and source links. |
| `python3 scripts/wiki_tool.py source-scan` | List all Raw sources and their coverage status. |
| `python3 scripts/wiki_tool.py source-scan --update --accept-covered` | Write/update `Schema/source-manifest.jsonl`. |
| `python3 scripts/wiki_tool.py source-lint` | Validate Raw source frontmatter and check processed sources have Wiki coverage. |
| `python3 scripts/wiki_tool.py source-delta` | Show Raw sources not yet in the manifest. |
| `python3 scripts/wiki_tool.py source-coverage` | Show which Raw sources are covered by Wiki notes. |
| `python3 scripts/wiki_tool.py search-catalog --query "text"` | Search compiled Wiki notes in the catalog. |
| `python3 scripts/wiki_tool.py log --title "title" --details "details"` | Append an entry to `Wiki/log.md`. |

## audit_public.py

| Command | What it does |
|---------|-------------|
| `python3 scripts/audit_public.py` | Fail if any tracked file contains secrets, private keys, or machine-local paths. |

## Maintenance Gate (run before every commit)

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

## After Source Ingest

```bash
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```
