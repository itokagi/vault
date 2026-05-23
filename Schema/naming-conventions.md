# Naming Conventions

## General Rules

- Use lowercase kebab-case for all file names: `my-note-name.md`
- No spaces in file names
- No special characters except hyphens
- Keep names short and descriptive

## Raw Sources

- Name after the content, not the author: `llm-wiki-overview.md` not `john-doe-notes.md`
- Include a date prefix for time-sensitive sources: `2024-01-15-gpt4-release-notes.md`

## Wiki Notes

| Type | Folder | Example |
|------|--------|---------|
| Topic | `Wiki/Topics/` | `machine-learning.md` |
| Concept | `Wiki/Concepts/` | `attention-mechanism.md` |
| Entity | `Wiki/Entities/` | `openai.md` |
| Project | `Wiki/Projects/` | `llm-wiki-build.md` |
| Log | `Wiki/Logs/` | `2024-01-15-ingest-session.md` |

## Schema Files

- Descriptive names, no date prefix: `frontmatter-schema.md`

## Scripts

- Use underscores for Python files: `wiki_tool.py`, `audit_public.py`
