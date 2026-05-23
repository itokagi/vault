# Skill: llm-wiki-query

Answer questions using the compiled Wiki. Minimise Raw source reads.

## When To Use

When the user asks a question that may be answered by existing Wiki knowledge.

## Steps

1. Start with `Wiki/index.md` to orient
2. Search the catalog:
   ```bash
   python3 scripts/wiki_tool.py search-catalog --query "user topic"
   ```
3. Open the most relevant Wiki notes (2–5 max)
4. If the compiled notes are sufficient, answer from them directly
5. If more detail is needed, open the specific Raw source listed in `sources`
6. Cite the Wiki note and the Raw source in the answer

## Rules

- Always search the catalog before opening Raw files
- Do not scan all of `Raw/Sources/` — open only files named in `sources`
- Do not answer from memory alone — cite what you found
