# Skill: llm-wiki-ingest

Process unprocessed Raw sources and compile them into Wiki notes.

## When To Use

When new files exist in `Raw/Sources/` with `Processed: false`.

## Steps

1. List files in `Raw/Sources/` where `Processed: false`
2. For each source:
   a. Run `search-catalog` to find related existing Wiki notes
   b. Open only the most relevant existing Wiki notes
   c. Create or update focused notes in the correct `Wiki/` subfolder
   d. Add the source path to the `sources` field of every note it informed
   e. Keep `source_count` accurate
3. Run checks:
   ```bash
   python3 scripts/wiki_tool.py build
   python3 scripts/wiki_tool.py lint
   python3 scripts/wiki_tool.py source-scan --update --accept-covered
   python3 scripts/wiki_tool.py source-lint
   ```
4. Add a log entry in `Wiki/Logs/` if the ingest meaningfully changed the Wiki
5. Commit with a descriptive message

## Rules

- Never modify files in `Raw/Sources/`
- Never invent claims not present in the source
- Every new Wiki note must have at least one entry in `sources`
- `source_count` must equal the length of `sources`
