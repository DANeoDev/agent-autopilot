#!/usr/bin/env python3
"""
Antigravity Autopilot - Dual-Tier Epistemic Memory & Decision Index (agy-memory)
Records and queries architectural decisions, invariant bedrock constraints ("Living Skeleton"),
and dynamic project experience ("Adaptive Outer Layer") with anti-sycophantic grounding.
"""

import sys
import os
import json
import uuid
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_MEMORY_DIR = Path.home() / ".gemini" / "autopilot" / "memory"
DEFAULT_MEMORY_FILE = DEFAULT_MEMORY_DIR / "memory.json"

# Foundational Bedrock Epistemic Invariants (Living Skeleton)
FOUNDATIONAL_SKELETON_INVARIANTS: List[Dict[str, Any]] = [
    {
        "id": "sk-0001",
        "title": "Empirical Grounding",
        "content": "Never fabricate test results, benchmark claims, or execution logs. Verification must be reproducible (exit code 0).",
        "tags": ["invariant", "empirical", "grounding", "bedrock"],
        "tier": "skeleton",
        "mutability": "protected",
        "author": "consensus",
        "project": "global",
        "version": 1
    },
    {
        "id": "sk-0002",
        "title": "Epistemic Friction",
        "content": "When human requirements contain technical contradictions, architectural anti-patterns, or regression risks, provide respectful technical friction rather than passive agreement.",
        "tags": ["invariant", "anti-sycophancy", "friction", "bedrock"],
        "tier": "skeleton",
        "mutability": "protected",
        "author": "consensus",
        "project": "global",
        "version": 1
    },
    {
        "id": "sk-0003",
        "title": "Boundary Separation",
        "content": "Strictly distinguish between metaphor/philosophical exploration and physical/computational invariants.",
        "tags": ["invariant", "boundary", "truth", "bedrock"],
        "tier": "skeleton",
        "mutability": "protected",
        "author": "consensus",
        "project": "global",
        "version": 1
    }
]


def get_memory_file(custom_path: Optional[Path] = None) -> Path:
    """Returns active memory file path, respecting environment overrides."""
    if custom_path:
        return Path(custom_path)
    env_override = os.environ.get("AUTOPILOT_MEMORY_FILE")
    if env_override:
        return Path(env_override)
    return DEFAULT_MEMORY_FILE


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


def migrate_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures backward compatibility by populating dual-tier schema defaults."""
    if "tier" not in entry:
        entry["tier"] = "adaptive"
    if "mutability" not in entry:
        entry["mutability"] = "protected" if entry["tier"] == "skeleton" else "mutable"
    if "author" not in entry:
        entry["author"] = "agent"
    if "version" not in entry:
        entry["version"] = 1
    if "project" not in entry:
        entry["project"] = "global"
    if "created_at" not in entry:
        entry["created_at"] = datetime.now(timezone.utc).isoformat()
    if "updated_at" not in entry:
        entry["updated_at"] = entry["created_at"]
    return entry


def load_memory(memory_path: Optional[Path] = None, auto_seed: bool = True) -> Dict[str, Any]:
    """Loads memory entries from disk, migrating legacy entries and auto-seeding bedrock invariants."""
    mem_file = get_memory_file(memory_path)
    mem: Dict[str, Any] = {"version": "2.0", "entries": []}

    if mem_file.exists():
        try:
            with open(mem_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict) and "entries" in loaded:
                    mem = loaded
                    mem["version"] = "2.0"
        except Exception:
            pass

    # Migrate any legacy entries missing dual-tier schema fields
    migrated_entries = [migrate_entry(e) for e in mem.get("entries", [])]
    existing_titles = {e["title"].lower() for e in migrated_entries}

    # Auto-seed foundational skeleton invariants if absent
    if auto_seed:
        for seed in FOUNDATIONAL_SKELETON_INVARIANTS:
            if seed["title"].lower() not in existing_titles:
                seed_copy = dict(seed)
                seed_copy["created_at"] = datetime.now(timezone.utc).isoformat()
                seed_copy["updated_at"] = seed_copy["created_at"]
                migrated_entries.insert(0, seed_copy)

    mem["entries"] = migrated_entries
    return mem


def save_memory(data: Dict[str, Any], memory_path: Optional[Path] = None):
    """Persists memory entries to disk."""
    mem_file = get_memory_file(memory_path)
    mem_file.parent.mkdir(parents=True, exist_ok=True)
    with open(mem_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_entry(
    title: str,
    content: str,
    tags: Optional[List[str]] = None,
    project: Optional[str] = None,
    tier: str = "adaptive",
    author: str = "agent",
    force_skeleton: bool = False,
    memory_path: Optional[Path] = None
) -> Tuple[Dict[str, Any], bool]:
    """
    Records or updates a memory entry with dual-tier protection and generous append semantics.
    Returns (entry_record, was_created_or_updated).
    Raises PermissionError if trying to mutate a protected skeleton without force_skeleton.
    """
    mem = load_memory(memory_path)
    proj = project or get_current_project_name()
    now_iso = datetime.now(timezone.utc).isoformat()
    clean_title = title.strip()
    clean_content = content.strip()
    clean_tags = [t.strip().lower() for t in (tags or [])]
    clean_tier = tier.lower() if tier.lower() in ("skeleton", "adaptive") else "adaptive"
    clean_author = author.lower() if author.lower() in ("human", "agent", "consensus") else "agent"

    # Check for existing entry with same title under same project (or global)
    existing_idx = None
    for idx, e in enumerate(mem["entries"]):
        if e["title"].lower() == clean_title.lower() and e.get("project", "").lower() == proj.lower():
            existing_idx = idx
            break

    if existing_idx is not None:
        existing = mem["entries"][existing_idx]
        is_skeleton = existing.get("tier") == "skeleton" or existing.get("mutability") == "protected"

        if is_skeleton and not force_skeleton:
            raise PermissionError(
                f"Safety Violation: Cannot mutate protected skeleton invariant '{existing['title']}' without --force-skeleton."
            )

        # Generous append / extension behavior
        existing["content"] = clean_content
        existing_tags = set(existing.get("tags", []))
        existing["tags"] = sorted(list(existing_tags.union(clean_tags)))
        existing["updated_at"] = now_iso
        existing["version"] = existing.get("version", 1) + 1
        existing["author"] = clean_author
        if force_skeleton and clean_tier == "skeleton":
            existing["tier"] = "skeleton"
            existing["mutability"] = "protected"

        save_memory(mem, memory_path)
        return existing, True

    # Create new entry
    entry_id = str(uuid.uuid4())[:8]
    mutability = "protected" if clean_tier == "skeleton" else "mutable"

    new_entry = {
        "id": entry_id,
        "project": proj,
        "tier": clean_tier,
        "mutability": mutability,
        "author": clean_author,
        "version": 1,
        "title": clean_title,
        "content": clean_content,
        "tags": clean_tags,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    mem["entries"].append(new_entry)
    save_memory(mem, memory_path)
    return new_entry, True


def delete_entry(entry_id: str, force_skeleton: bool = False, memory_path: Optional[Path] = None) -> bool:
    """
    Deletes a memory entry.
    Raises PermissionError if attempting to delete a skeleton entry without force_skeleton.
    """
    mem = load_memory(memory_path)
    target_idx = None

    for idx, e in enumerate(mem["entries"]):
        if e.get("id") == entry_id:
            target_idx = idx
            break

    if target_idx is None:
        return False

    entry = mem["entries"][target_idx]
    is_skeleton = entry.get("tier") == "skeleton" or entry.get("mutability") == "protected"

    if is_skeleton and not force_skeleton:
        raise PermissionError(
            f"Safety Violation: Cannot delete protected skeleton invariant [{entry_id}] ('{entry['title']}') without --force-skeleton."
        )

    mem["entries"].pop(target_idx)
    save_memory(mem, memory_path)
    return True


def search_entries(
    query: str,
    project_filter: Optional[str] = None,
    tier_filter: Optional[str] = None,
    memory_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Searches memory entries filtered by query, project, and tier."""
    mem = load_memory(memory_path)
    q_terms = [t.lower() for t in query.split()]
    matches = []

    for e in mem.get("entries", []):
        # Project filter: specific project or global bedrock
        if project_filter and e.get("project", "").lower() not in (project_filter.lower(), "global"):
            continue

        # Tier filter
        if tier_filter and e.get("tier", "").lower() != tier_filter.lower():
            continue

        searchable = f"{e.get('title', '')} {e.get('content', '')} {' '.join(e.get('tags', []))} {e.get('project', '')} {e.get('tier', '')}".lower()
        score = sum(1 for term in q_terms if term in searchable)
        if score > 0 or not q_terms:
            matches.append((score, e))

    # Sort by score descending, then skeleton tier first, then newest
    matches.sort(key=lambda x: (x[0], 1 if x[1].get("tier") == "skeleton" else 0, x[1].get("updated_at", "")), reverse=True)
    return [m[1] for m in matches]


def get_memory_stats(project_filter: Optional[str] = None, memory_path: Optional[Path] = None) -> Dict[str, Any]:
    """Returns counts of skeleton invariants and adaptive learnings."""
    mem = load_memory(memory_path)
    entries = mem.get("entries", [])
    if project_filter:
        entries = [e for e in entries if e.get("project", "").lower() in (project_filter.lower(), "global")]

    skeleton_count = sum(1 for e in entries if e.get("tier") == "skeleton")
    adaptive_count = sum(1 for e in entries if e.get("tier") != "skeleton")

    return {
        "total": len(entries),
        "skeleton_count": skeleton_count,
        "adaptive_count": adaptive_count,
        "entries": entries
    }


def format_entry_card(e: Dict[str, Any]) -> str:
    """Formats a memory entry as a clean, tier-aware ASCII card."""
    tier = e.get("tier", "adaptive").upper()
    mutability = e.get("mutability", "mutable").upper()
    version = e.get("version", 1)
    author = e.get("author", "agent")
    tags_str = ", ".join(e.get("tags", [])) if e.get("tags") else "none"
    updated = e.get("updated_at", e.get("created_at", ""))[:19].replace("T", " ")

    if tier == "SKELETON":
        badge = f"⚓ SKELETON BEDROCK [MUTABILITY: {mutability}]"
    else:
        badge = f"🌱 ADAPTIVE EXPERIENCE [v{version} • AUTHOR: {author}]"

    lines = [
        f"┌─ [{e['id']}] {e['title']} ({e['project']}) ────────────────────────┐",
        f"│ Tier    : {badge:<62} │",
        f"│ Updated : {updated:<62} │",
        f"│ Tags    : {tags_str:<62} │",
        "├─────────────────────────────────────────────────────────────────────────────┤"
    ]
    content = e.get("content", "")
    for line in content.splitlines():
        while len(line) > 71:
            lines.append(f"│ {line[:71]:<71} │")
            line = line[71:]
        lines.append(f"│ {line:<71} │")
    lines.append("└─────────────────────────────────────────────────────────────────────────────┘")
    return "\n".join(lines)


def render_context_injection(project: Optional[str] = None, tier_filter: Optional[str] = None, limit: int = 6) -> str:
    """Renders a concise markdown block of architectural memory for agent prompt injection."""
    proj = project or get_current_project_name()
    entries = search_entries("", project_filter=proj, tier_filter=tier_filter)

    if not entries:
        return ""

    skeletons = [e for e in entries if e.get("tier") == "skeleton"]
    adaptives = [e for e in entries if e.get("tier") != "skeleton"]

    lines = [
        "### 🧠 Persistent Epistemic Invariants & Architectural Memory (Autopilot)",
        ""
    ]

    if skeletons:
        lines.append("#### ⚓ Epistemic Bedrock (Living Skeleton - Invariants):")
        for e in skeletons[:4]:
            lines.append(f"- **{e['title']}**: {e['content']}")
        lines.append("")

    if adaptives:
        lines.append("#### 🌱 Project Conventions & Discoveries (Adaptive Layer):")
        for e in adaptives[:max(2, limit - len(skeletons))]:
            lines.append(f"- **{e['title']}** (v{e.get('version', 1)}): {e['content']}")
        lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Autopilot - Dual-Tier Epistemic Memory Index")
    subparsers = parser.add_subparsers(dest="command", help="Memory subcommand to execute")

    # record
    p_record = subparsers.add_parser("record", help="Record or update an architectural decision or invariant")
    p_record.add_argument("title", type=str, help="Title of the decision or invariant")
    p_record.add_argument("content", type=str, help="Detailed constraint, invariant, or convention")
    p_record.add_argument("--tier", choices=["skeleton", "adaptive"], default="adaptive", help="Memory tier: skeleton (bedrock) or adaptive (default)")
    p_record.add_argument("--author", choices=["human", "agent", "consensus"], default="agent", help="Author provenance")
    p_record.add_argument("--tags", nargs="*", default=[], help="Classification tags")
    p_record.add_argument("--project", type=str, default=None, help="Project name (defaults to active repo)")
    p_record.add_argument("--force-skeleton", action="store_true", help="Force mutation of protected skeleton invariants")

    # search
    p_search = subparsers.add_parser("search", help="Search memory entries by keywords")
    p_search.add_argument("query", nargs="*", default=[], help="Keywords to search")
    p_search.add_argument("--tier", choices=["skeleton", "adaptive"], default=None, help="Filter by tier")
    p_search.add_argument("--project", type=str, default=None, help="Filter by project")

    # list
    p_list = subparsers.add_parser("list", help="List stored memory entries")
    p_list.add_argument("--tier", choices=["skeleton", "adaptive"], default=None, help="Filter by tier")
    p_list.add_argument("--project", type=str, default=None, help="Filter by project")
    p_list.add_argument("--json", action="store_true", help="Output entries as raw JSON")

    # inject
    p_inject = subparsers.add_parser("inject", help="Output prompt-injection markdown context")
    p_inject.add_argument("--tier", choices=["skeleton", "adaptive"], default=None, help="Filter by tier")
    p_inject.add_argument("--project", type=str, default=None, help="Filter by project")

    # delete
    p_del = subparsers.add_parser("delete", help="Delete a memory entry by ID")
    p_del.add_argument("entry_id", type=str, help="ID of entry to delete")
    p_del.add_argument("--force-skeleton", action="store_true", help="Required to delete protected skeleton invariants")

    args = parser.parse_args()

    if args.command == "record":
        try:
            entry, is_new = record_entry(
                title=args.title,
                content=args.content,
                tags=args.tags,
                project=args.project,
                tier=args.tier,
                author=args.author,
                force_skeleton=args.force_skeleton
            )
            tier_badge = "⚓ SKELETON" if entry["tier"] == "skeleton" else "🌱 ADAPTIVE"
            print(f"[SUCCESS] Recorded {tier_badge} memory [{entry['id']}]: '{entry['title']}' (v{entry['version']}) for project '{entry['project']}'")
        except PermissionError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.command == "search":
        q = " ".join(args.query).strip()
        results = search_entries(q, project_filter=args.project, tier_filter=args.tier)
        print(f"\n========================================================")
        print(f"  AUTOPILOT MEMORY SEARCH: '{q}' ({len(results)} found)")
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
        tier_filter = getattr(args, "tier", None)
        as_json = getattr(args, "json", False)

        entries = search_entries("", project_filter=proj, tier_filter=tier_filter)
        if as_json:
            print(json.dumps(entries, indent=2))
            return

        stats = get_memory_stats(project_filter=proj)
        print(f"\n========================================================")
        print(f"  AUTOPILOT EPISTEMIC MEMORY ({stats['skeleton_count']} Skeleton, {stats['adaptive_count']} Adaptive)")
        print(f"========================================================\n")
        if not entries:
            print("  No memory entries matching criteria.")
        else:
            for r in entries:
                print(format_entry_card(r))
                print()
        return

    if args.command == "inject":
        print(render_context_injection(project=args.project, tier_filter=args.tier))
        return

    if args.command == "delete":
        try:
            success = delete_entry(args.entry_id, force_skeleton=args.force_skeleton)
            if success:
                print(f"[SUCCESS] Deleted memory entry [{args.entry_id}]")
            else:
                print(f"[ERROR] Entry ID [{args.entry_id}] not found", file=sys.stderr)
                sys.exit(1)
        except PermissionError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
        return


if __name__ == "__main__":
    main()
