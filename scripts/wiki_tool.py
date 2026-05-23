#!/usr/bin/env python3
"""wiki_tool.py — deterministic maintenance tool for the LLM Wiki. Standard library only."""

import sys
import os
import json
import re
import argparse
from pathlib import Path
from datetime import date as _date

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "Wiki"
RAW_SOURCES_DIR = VAULT_ROOT / "Raw" / "Sources"
SCHEMA_DIR = VAULT_ROOT / "Schema"
CATALOG_PATH = WIKI_DIR / "catalog.jsonl"
SOURCE_MANIFEST_PATH = SCHEMA_DIR / "source-manifest.jsonl"
WIKI_INDEX_PATH = WIKI_DIR / "index.md"
WIKI_LOG_PATH = WIKI_DIR / "log.md"

ALLOWED_TAGS = {"topic", "concept", "entity", "project", "log"}
WIKI_SUBFOLDERS = ["Topics", "Concepts", "Entities", "Projects", "Logs"]
REQUIRED_SOURCE_FIELDS = {"Title", "Reference", "Created", "Processed", "tags"}
REQUIRED_WIKI_FIELDS = {"tags", "sources", "source_count", "created", "updated"}
GENERATED_NAMES = {"index.md", "log.md"}

TODAY = _date.today().isoformat()


# ── Frontmatter parser ───────────────────────────────────────────────────────

def parse_frontmatter(text):
    """Parse YAML frontmatter. Returns (dict, body). No external deps."""
    if not text.startswith("---"):
        return {}, text

    lines = text.split("\n")
    end = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end = i
            break

    if end == -1:
        return {}, text

    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])
    result = {}
    current_list = None

    for line in fm_lines:
        stripped = line.strip()
        if not stripped:
            continue

        # List item
        if stripped.startswith("- "):
            val = stripped[2:].strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(val)
            continue

        # Key: value
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")

            if val == "":
                result[key] = []
                current_list = result[key]
            elif val.lower() == "true":
                result[key] = True
                current_list = None
            elif val.lower() == "false":
                result[key] = False
                current_list = None
            else:
                try:
                    result[key] = int(val)
                except ValueError:
                    result[key] = val
                current_list = None

    return result, body


# ── Helpers ──────────────────────────────────────────────────────────────────

def relative(path):
    return str(Path(path).relative_to(VAULT_ROOT)).replace("\\", "/")


def strip_wikilink(val):
    """Strip [[...]] or [[...|display]] syntax to plain text."""
    if isinstance(val, str):
        match = re.match(r"^\[\[([^\]|]+)(?:\|[^\]]+)?\]\]$", val.strip())
        return match.group(1) if match else val
    return val


def clean_list(val):
    """Return a list with wikilink syntax stripped."""
    if isinstance(val, list):
        return [strip_wikilink(v) for v in val]
    if isinstance(val, str):
        return [strip_wikilink(val)]
    return []


def get_wiki_notes():
    notes = []
    for subfolder in WIKI_SUBFOLDERS:
        folder = WIKI_DIR / subfolder
        if folder.exists():
            notes.extend(
                p for p in folder.glob("*.md")
                if p.name not in GENERATED_NAMES and p.name != ".gitkeep"
            )
    return notes


def get_raw_sources():
    if not RAW_SOURCES_DIR.exists():
        return []
    return [
        f for f in RAW_SOURCES_DIR.glob("*.md")
        if f.name not in (".gitkeep",)
    ]


def build_coverage_map(wiki_notes):
    """Return dict: source_rel_path -> [wiki_note_rel_paths]."""
    coverage = {}
    for note_path in wiki_notes:
        text = note_path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        for src in clean_list(fm.get("sources", [])):
            coverage.setdefault(src, []).append(relative(note_path))
    return coverage


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_doctor():
    errors = []

    if sys.version_info >= (3, 8):
        print(f"  python {sys.version_info.major}.{sys.version_info.minor} OK")
    else:
        errors.append(f"Python 3.8+ required, got {sys.version}")

    required_folders = [
        WIKI_DIR, RAW_SOURCES_DIR, SCHEMA_DIR,
        VAULT_ROOT / "_templates",
        VAULT_ROOT / ".agents" / "skills",
        VAULT_ROOT / "scripts",
    ]
    for folder in required_folders:
        if folder.exists():
            print(f"  folder OK: {relative(folder)}")
        else:
            errors.append(f"missing folder: {relative(folder)}")

    if CATALOG_PATH.exists():
        count = sum(1 for l in CATALOG_PATH.read_text().splitlines() if l.strip())
        print(f"  catalog OK: {count} entries")
    else:
        print("  catalog: not found (run build)")

    if SOURCE_MANIFEST_PATH.exists():
        count = sum(1 for l in SOURCE_MANIFEST_PATH.read_text().splitlines() if l.strip())
        print(f"  source-manifest OK: {count} entries")
    else:
        print("  source-manifest: not found (run source-scan --update)")

    wiki_notes = get_wiki_notes()
    raw_sources = get_raw_sources()
    print(f"  wiki notes: {len(wiki_notes)}")
    print(f"  raw sources: {len(raw_sources)}")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    print("doctor: all checks passed")


def cmd_build():
    wiki_notes = get_wiki_notes()
    catalog_entries = []

    for note_path in wiki_notes:
        text = note_path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        tag = tags[0] if tags else "unknown"

        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else note_path.stem

        sources = clean_list(fm.get("sources", []))

        catalog_entries.append({
            "path": relative(note_path),
            "title": title,
            "tag": tag,
            "topics": clean_list(fm.get("topics", [])),
            "sources": sources,
            "updated": fm.get("updated", TODAY),
        })

    WIKI_DIR.mkdir(exist_ok=True)
    with CATALOG_PATH.open("w", encoding="utf-8") as f:
        for entry in catalog_entries:
            f.write(json.dumps(entry) + "\n")
    print(f"build: catalog written — {len(catalog_entries)} entries")

    # Wiki/index.md
    lines = [f"# Wiki Index\n\n", f"Generated: {TODAY} | Notes: {len(catalog_entries)}\n\n"]
    for subfolder in WIKI_SUBFOLDERS:
        folder_entries = [e for e in catalog_entries if e["path"].startswith(f"Wiki/{subfolder}/")]
        lines.append(f"## {subfolder} ({len(folder_entries)})\n\n")
        for e in folder_entries:
            lines.append(f"- [[{Path(e['path']).stem}]] — {e['title']}\n")
        lines.append("\n")
    WIKI_INDEX_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"build: wrote {relative(WIKI_INDEX_PATH)}")

    # Per-folder indexes
    for subfolder in WIKI_SUBFOLDERS:
        folder = WIKI_DIR / subfolder
        if not folder.exists():
            continue
        folder_entries = [e for e in catalog_entries if e["path"].startswith(f"Wiki/{subfolder}/")]
        index_path = folder / "index.md"
        idx_lines = [f"# {subfolder}\n\n"]
        for e in folder_entries:
            idx_lines.append(f"- [[{Path(e['path']).stem}]] — {e['title']}\n")
        index_path.write_text("".join(idx_lines), encoding="utf-8")
        print(f"build: wrote {relative(index_path)}")


def cmd_lint():
    errors = []
    wiki_notes = get_wiki_notes()

    for note_path in wiki_notes:
        text = note_path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        rel = relative(note_path)

        for field in REQUIRED_WIKI_FIELDS:
            if field not in fm:
                errors.append(f"{rel}: missing field '{field}'")

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        if not tags:
            errors.append(f"{rel}: no tags")
        elif tags[0] not in ALLOWED_TAGS:
            errors.append(f"{rel}: disallowed tag '{tags[0]}'")

        sources = clean_list(fm.get("sources", []))
        source_count = fm.get("source_count", None)
        if source_count is not None and source_count != len(sources):
            errors.append(f"{rel}: source_count={source_count} but {len(sources)} source(s) listed")

        for src in sources:
            if not (VAULT_ROOT / src).exists():
                errors.append(f"{rel}: source not found: {src}")

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"lint: {len(errors)} error(s)")
        sys.exit(1)
    print(f"lint: {len(wiki_notes)} notes checked, all passed")


def cmd_source_scan(update=False, accept_covered=False):
    raw_sources = get_raw_sources()
    wiki_notes = get_wiki_notes()
    coverage = build_coverage_map(wiki_notes)

    entries = []
    for src_path in raw_sources:
        text = src_path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        rel = relative(src_path)
        covered_by = coverage.get(rel, [])
        entry = {
            "path": rel,
            "title": fm.get("Title", src_path.stem),
            "processed": fm.get("Processed", False),
            "covered_by": covered_by,
            "updated": TODAY,
        }
        entries.append(entry)
        status = f"covered by {len(covered_by)}" if covered_by else "not covered"
        print(f"  {rel} — processed={entry['processed']}, {status}")

    if update:
        SCHEMA_DIR.mkdir(exist_ok=True)
        with SOURCE_MANIFEST_PATH.open("w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
        print(f"source-scan: manifest written — {len(entries)} entries")
    else:
        print(f"source-scan: {len(entries)} source(s) found (use --update to write manifest)")


def cmd_source_lint():
    errors = []
    raw_sources = get_raw_sources()
    wiki_notes = get_wiki_notes()
    coverage = build_coverage_map(wiki_notes)

    for src_path in raw_sources:
        text = src_path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        rel = relative(src_path)

        for field in REQUIRED_SOURCE_FIELDS:
            if field not in fm:
                errors.append(f"{rel}: missing field '{field}'")

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        if "source" not in tags:
            errors.append(f"{rel}: tags must include 'source'")

        if fm.get("Processed", False) and rel not in coverage:
            errors.append(f"{rel}: Processed=true but no Wiki note covers it")

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"source-lint: {len(errors)} error(s)")
        sys.exit(1)
    print(f"source-lint: {len(raw_sources)} source(s) checked, all passed")


def cmd_source_delta():
    if not SOURCE_MANIFEST_PATH.exists():
        print("source-delta: no manifest (run source-scan --update first)")
        return
    manifest_paths = set()
    for line in SOURCE_MANIFEST_PATH.read_text().splitlines():
        if line.strip():
            manifest_paths.add(json.loads(line)["path"])
    missing = [relative(s) for s in get_raw_sources() if relative(s) not in manifest_paths]
    if missing:
        print(f"source-delta: {len(missing)} source(s) not in manifest:")
        for m in missing:
            print(f"  {m}")
    else:
        print("source-delta: all sources are in the manifest")


def cmd_source_coverage():
    wiki_notes = get_wiki_notes()
    coverage = build_coverage_map(wiki_notes)
    for src_path in get_raw_sources():
        rel = relative(src_path)
        covered = coverage.get(rel, [])
        status = f"covered ({len(covered)} note(s))" if covered else "NOT COVERED"
        print(f"  {rel}: {status}")


def cmd_search_catalog(query):
    if not CATALOG_PATH.exists():
        print("search-catalog: catalog not found (run build first)")
        return
    query_lower = query.lower()
    results = []
    for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        searchable = " ".join([
            entry.get("title", ""),
            entry.get("tag", ""),
            " ".join(entry.get("topics", [])),
            entry.get("path", ""),
        ]).lower()
        if query_lower in searchable:
            results.append(entry)
    if results:
        print(f"search-catalog: {len(results)} result(s) for '{query}'")
        for r in results:
            print(f"  [{r['tag']}] {r['title']} — {r['path']}")
    else:
        print(f"search-catalog: no results for '{query}'")


def cmd_log(title, details):
    entry = f"\n## {TODAY} — {title}\n\n{details}\n"
    if WIKI_LOG_PATH.exists():
        WIKI_LOG_PATH.write_text(
            WIKI_LOG_PATH.read_text(encoding="utf-8") + entry, encoding="utf-8"
        )
    else:
        WIKI_DIR.mkdir(exist_ok=True)
        WIKI_LOG_PATH.write_text(f"# Wiki Log\n{entry}", encoding="utf-8")
    print(f"log: appended '{title}'")


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LLM Wiki maintenance tool")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")
    sub.add_parser("build")
    sub.add_parser("lint")

    p_scan = sub.add_parser("source-scan")
    p_scan.add_argument("--update", action="store_true")
    p_scan.add_argument("--accept-covered", action="store_true")

    sub.add_parser("source-lint")
    sub.add_parser("source-delta")
    sub.add_parser("source-coverage")

    p_search = sub.add_parser("search-catalog")
    p_search.add_argument("--query", required=True)

    p_log = sub.add_parser("log")
    p_log.add_argument("--title", required=True)
    p_log.add_argument("--details", required=True)

    args = parser.parse_args()
    {
        "doctor": cmd_doctor,
        "build": cmd_build,
        "lint": cmd_lint,
        "source-lint": cmd_source_lint,
        "source-delta": cmd_source_delta,
        "source-coverage": cmd_source_coverage,
    }.get(args.command, lambda: None)()

    if args.command == "source-scan":
        cmd_source_scan(update=args.update, accept_covered=args.accept_covered)
    elif args.command == "search-catalog":
        cmd_search_catalog(args.query)
    elif args.command == "log":
        cmd_log(args.title, args.details)


if __name__ == "__main__":
    main()
