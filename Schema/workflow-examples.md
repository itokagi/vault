# Workflow Examples

## Example 1: Ingesting a New Source

You have an article saved as `Raw/Sources/attention-is-all-you-need.md`.

**Step 1 — Search the catalog first:**
```bash
python3 scripts/wiki_tool.py search-catalog --query "attention transformer"
```

**Step 2 — Open relevant existing Wiki notes** (if any match).

**Step 3 — Create new Wiki notes** for key concepts not yet covered:

`Wiki/Concepts/attention-mechanism.md`
```yaml
---
tags:
  - "concept"
topics: ["machine-learning"]
status: seed
created: 2024-01-15
updated: 2024-01-15
sources: ["Raw/Sources/attention-is-all-you-need.md"]
source_count: 1
aliases: ["self-attention"]
---

The attention mechanism allows a model to weigh the relevance of each part of the input when producing an output.
```

**Step 4 — Run checks:**
```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```

---

## Example 2: Answering a Question From the Wiki

User asks: *"What is the attention mechanism?"*

**Step 1:**
```bash
python3 scripts/wiki_tool.py search-catalog --query "attention mechanism"
```

**Step 2** — Open `Wiki/Concepts/attention-mechanism.md`.

**Step 3** — Answer from the compiled note. If more detail is needed, open `Raw/Sources/attention-is-all-you-need.md`.

**Step 4** — Cite both: the Wiki note and the Raw source.
