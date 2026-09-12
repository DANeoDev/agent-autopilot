#!/usr/bin/env python3
"""
Antigravity Autopilot - Cross-Project Architectural Memory & Decision Index (agy-memory)
Records and queries architectural decisions, project patterns, and user conventions
across workspaces on this machine, providing persistent memory across agent sessions.
"""

import sys
import os
import json
import uuid
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_MEMORY_DIR = Path.home() / ".gemini" / "autopilot" / "memory"
DEFAULT_MEMORY_FILE = DEFAULT_MEMORY_DIR / "memory.json"


def get_current_project_name() -> str:
    """Infers current project name from git repo root or current directory."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if res.returncode == 0 and res.stdout.strip():
            return Path(res.stdout.strip()).name
    except Exception:
        pass
    return Path.cwd().name


def load_memory() -> Dict[str, Any]:
    """Loads memory entries from memory.json."""
    if DEFAULT_MEMORY_FILE.exists():
        try:
            with open(DEFAULT_MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": "1.0", "entries": []}


def save_memory(data: Dict[str, Any]):
    """Persists memory entries to memory.json."""
    DEFAULT_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    with open(DEFAULT_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_entry(title: str, content: str, tags: Optional[List[str]] = None, project: Optional[str] = None) -> Dict[str, Any]:
    """Records a new architectural decision or project pattern."""
    mem = load_memory()
    proj = project or get_current_project_name()
    now_iso = datetime.now(timezone.utc).isoformat()
    entry_id = str(uuid.uuid4())[:8]

    entry = {
        "id": entry_id,
        "project": proj,
        "title": title.strip(),
        "content": content.strip(),
        "tags": [t.strip().lower() for t in (tags or [])],
        "created_at": now_iso
    }

    mem["entries"].append(entry)
    save_memory(mem)
    return entry


def search_entries(query: str, project_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Searches memory entries by query terms and optional project filter."""
    mem = load_memory()
    q_terms = [t.lower() for t in query.split()]
    matches = []

    for e in mem.get("entries", []):
        if project_filter and e.get("project", "").lower() != project_filter.lower():
            continue

        searchable = f"{e.get('title', '')} {e.get('content', '')} {' '.join(e.get('tags', []))} {e.get('project', '')}".lower()
        score = sum(1 for term in q_terms if term in searchable)
        if score > 0 or not q_terms:
            matches.append((score, e))

    matches.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matches]


def format_entry_card(e: Dict[str, Any]) -> str:
    """Formats a single memory entry as an ASCII card."""
    tags_str = ", ".join(e.get("tags", [])) if e.get("tags") else "none"
    created = e.get("created_at", "")[:19].replace("T", " ")
    lines = [
        f"┌─ [{e['id']}] {e['title']} ({e['project']}) ────────────────────────┐",
        f"│ Created : {created:<62} │",
        f"│ Tags    : {tags_str:<62} │",
        "├─────────────────────────────────────────────────────────────────────────────┤"
    ]
    # Wrap content lines
    content = e.get("content", "")
    for line in content.splitlines():
        while len(line) > 71:
            lines.append(f"│ {line[:71]:<71} │")
            line = line[71:]
        lines.append(f"│ {line:<71} │")
    lines.append("└─────────────────────────────────────────────────────────────────────────────┘")
    return "\n".join(lines)


def render_context_injection(project: Optional[str] = None, limit: int = 5) -> str:
    """Renders a concise markdown block of architectural decisions for prompt injection."""
    proj = project or get_current_project_name()
    entries = search_entries("", project_filter=proj)
    if not entries:
        # Fallback to general cross-project entries
        entries = load_memory().get("entries", [])

    if not entries:
        return ""

    lines = [
        "### 🧠 Persistent Architectural Decisions & Conventions (Autopilot Memory)",
        ""
    ]
    for e in entries[:limit]:
        tags = f" `[{', '.join(e.get('tags', []))}]`" if e.get("tags") else ""
        lines.append(f"- **{e['title']}** ({e['project']}){tags}: {e['content']}")
    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Autopilot - Cross-Project Architectural Memory & Decision Index")
    subparsers = parser.add_subparsers(dest="command", help="Memory subcommand to execute")

    # record
    p_record = subparsers.add_parser("record", help="Record an architectural decision or project convention")
    p_record.add_argument("title", type=str, help="Brief title of the architectural decision")
    p_record.add_argument("content", type=str, help="Detailed explanation, convention, or rule")
    p_record.add_argument("--tags", nargs="*", default=[], help="Tags for classification (e.g. auth, api, db)")
    p_record.add_argument("--project", type=str, default=None, help="Project name (defaults to current repository)")

    # search
    p_search = subparsers.add_parser("search", help="Search recorded architectural decisions")
    p_search.add_argument("query", nargs="*", default=[], help="Search query keywords")
    p_search.add_argument("--project", type=str, default=None, help="Filter by project name")

    # list
    p_list = subparsers.add_parser("list", help="List all stored decisions")
    p_list.add_argument("--project", type=str, default=None, help="Filter by project name")

    # inject
    p_inject = subparsers.add_parser("inject", help="Output decisions as a concise markdown block for prompt injection")
    p_inject.add_argument("--project", type=str, default=None, help="Filter by project name")

    # delete
    p_del = subparsers.add_parser("delete", help="Delete a recorded memory entry by ID")
    p_del.add_argument("entry_id", type=str, help="ID of the entry to remove")

    args = parser.parse_args()

    if args.command == "record":
        e = record_entry(args.title, args.content, tags=args.tags, project=args.project)
        print(f"[SUCCESS] Recorded architectural decision [{e['id']}]: '{e['title']}' for project '{e['project']}'")
        return

    if args.command == "search":
        q = " ".join(args.query).strip()
        results = search_entries(q, project_filter=args.project)
        print(f"\n========================================================")
        print(f"  AUTOPILOT ARCHITECTURAL MEMORY SEARCH: '{q}' ({len(results)} found)")
        print(f"========================================================\n")
        if not results:
            print("  No matching decisions found.")
        else:
            for r in results:
                print(format_entry_card(r))
                print()
        return

    if args.command == "list" or not args.command:
        proj = getattr(args, "project", None)
        entries = search_entries("", project_filter=proj)
        print(f"\n========================================================")
        print(f"  AUTOPILOT STORED ARCHITECTURAL MEMORY ({len(entries)} entries)")
        print(f"========================================================\n")
        if not entries:
            print("  No architectural memories recorded yet.")
            print("  Use: agy-memory record \"Title\" \"Content description...\"")
        else:
            for r in entries:
                print(format_entry_card(r))
                print()
        return

    if args.command == "inject":
        print(render_context_injection(project=args.project))
        return

    if args.command == "delete":
        mem = load_memory()
        initial_len = len(mem.get("entries", []))
        mem["entries"] = [e for e in mem.get("entries", []) if e.get("id") != args.entry_id]
        if len(mem["entries"]) < initial_len:
            save_memory(mem)
            print(f"[SUCCESS] Deleted memory entry [{args.entry_id}]")
        else:
            print(f"[ERROR] Entry ID [{args.entry_id}] not found")
        return


if __name__ == "__main__":
    main()
