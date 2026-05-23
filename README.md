# Vault

A personal knowledge base built for both humans and AI agents, using the LLM Wiki system inside Obsidian.

## What This Is

Most notes apps pile everything into one place. This vault separates **source material** from **compiled knowledge**:

- **Raw** — the original stuff you feed in (articles, transcripts, docs, research). Never edited.
- **Wiki** — clean, reusable notes compiled from Raw sources by you or an AI agent. Every claim links back to where it came from.

The result: an AI agent can search the Wiki first, find what it needs in seconds, and only dig into Raw sources when it needs more detail. No hallucinations, no made-up citations.

## Folder Structure

```
Raw/
  Sources/    ← drop source material here (markdown files)
  Files/      ← attachments (images, PDFs)

Wiki/
  Topics/     ← broad subject areas
  Concepts/   ← specific ideas or terms
  Entities/   ← people, places, organisations
  Projects/   ← project-specific knowledge
  Logs/       ← change logs and session notes

Schema/       ← rules for how notes must be structured
_templates/   ← blank note templates to copy from
.agents/      ← instructions and skills for AI agents
scripts/      ← automation tools (wiki_tool.py lives here)
tutorial/     ← tutorial files for the setup process
```

## How To Use It

### Adding a source

1. Put a cleaned markdown file into `Raw/Sources/`
2. Tell an agent: *"Compile any unprocessed Raw sources into Wiki notes"*
3. The agent reads the source, writes focused notes into `Wiki/`, and links every note back to the source file

### Asking a question

1. Tell an agent: *"Search the Wiki for [topic] and answer my question"*
2. The agent searches `Wiki/catalog.jsonl` first — no broad context scanning
3. It opens only the relevant Wiki notes, then Raw sources only if needed
4. Every answer comes with a traceable source link

### Running checks

Before any meaningful commit, run:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

## Working With AI Agents (Claude Code)

Open this vault folder in Claude Code. The agent will:

- Read `AGENTS.md` first to understand the rules
- Search the catalog before opening any Raw files
- Only write compiled notes into `Wiki/` — never modify Raw sources
- Keep every claim linked to a source
- Run the maintenance checks before committing

To kick off a session:

```
Read AGENTS.md and inspect the current LLM Wiki. Search the catalog before opening Raw sources. Compile any unprocessed Raw sources into concise Wiki notes, keep every claim linked to sources, rebuild indexes, run lint/source checks, and summarise what changed.
```

## Based On

This vault follows the [LLM Wiki Core Setup Guide](https://github.com/wanderloots-tutorials/vibe-coding/blob/main/wanderloots-llm-wiki-core-setup-v1.0.0.md) by Wanderloots. The guide defines the full build order, folder structure, schema contracts, and agent workflows used here.

## Setup Progress

| Step | Status | Description |
|------|--------|-------------|
| 00 | Done | Empty vault, .gitignore, Welcome note |
| 01 | Done | Core folder structure |
| 02 | Pending | AGENTS.md, Schema rules, Agent skills |
| 03 | Pending | Note templates |
| 04 | Pending | wiki_tool.py automation |
| 05 | Pending | First source ingest |
| 06 | Pending | Full lint and query pass |
