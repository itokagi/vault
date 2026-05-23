# Skill: llm-wiki-ingest

Process unprocessed Raw sources and compile them into Wiki notes.

> Requires the **obsidian-markdown** skill for correct note formatting. Apply its wikilink, callout, and properties rules when creating every note.

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

## Wikilink Rules (from obsidian-markdown skill)

- Use `[[Note Name]]` or `[[Note Name|Display Text]]` for all internal vault links — never plain text or Markdown links for internal notes
- Use `[[Note Name|Display Text]]` when the file name alone is unclear
- Add a `## Source` section at the bottom of every Wiki note with `[[Source File Name]]` — this creates backlinks in Obsidian
- In frontmatter `topics` lists, use `"[[topic-note-name]]"` syntax so Obsidian tracks them as link properties
- Keep `sources` frontmatter as plain file paths (e.g. `Raw/Sources/file.md`) so wiki_tool.py can verify them
- Use `> [!callout-type]` for key quotes, tips, or warnings from the source
- Ensure all cross-links between related Wiki notes are bidirectional and complete

## Rules

- Never modify files in `Raw/Sources/`
- Never invent claims not present in the source
- Every new Wiki note must have at least one entry in `sources`
- `source_count` must equal the length of `sources`
