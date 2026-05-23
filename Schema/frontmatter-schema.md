# Frontmatter Schema

## Source Notes (`Raw/Sources/`)

```yaml
---
Title: ""
Author: ""
Reference: ""
ContentType:
  - "markdown"
Created: YYYY-MM-DD
Processed: false
tags:
  - "source"
---
```

| Field | Required | Description |
|-------|----------|-------------|
| Title | Yes | Human-readable title of the source |
| Author | Yes | Author name or "unknown" |
| Reference | Yes | URL, ISBN, or unique identifier |
| ContentType | Yes | Format of the source |
| Created | Yes | Date the source was added |
| Processed | Yes | `false` until compiled into Wiki notes |
| tags | Yes | Must include `source` |

## Compiled Wiki Notes (`Wiki/`)

```yaml
---
tags:
  - "concept"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---
```

| Field | Required | Description |
|-------|----------|-------------|
| tags | Yes | Exactly one allowed tag (see below) |
| topics | Yes | Related topic note names |
| status | Yes | `seed`, `growing`, or `evergreen` |
| created | Yes | Date note was first created |
| updated | Yes | Date note was last updated |
| sources | Yes | Paths to Raw source files that support this note |
| source_count | Yes | Must equal the number of entries in `sources` |
| aliases | No | Alternative names for this note |

## Allowed Wiki Tags

| Tag | Folder | Use for |
|-----|--------|---------|
| `topic` | `Wiki/Topics/` | Broad subject areas |
| `concept` | `Wiki/Concepts/` | Specific ideas or terms |
| `entity` | `Wiki/Entities/` | People, places, organisations |
| `project` | `Wiki/Projects/` | Project-specific knowledge |
| `log` | `Wiki/Logs/` | Change logs and session notes |
