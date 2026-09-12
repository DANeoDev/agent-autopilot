"""
Automated Test Suite for Dual-Tier Epistemic Memory & Anti-Sycophantic Grounding
Compatible with both pytest and Python standard library unittest.
Tests schema integrity, protection barriers, generous append semantics,
search/filtering by tier, and backward compatibility.
"""

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bin.agy_memory import (
    load_memory,
    save_memory,
    record_entry,
    delete_entry,
    search_entries,
    get_memory_stats,
    FOUNDATIONAL_SKELETON_INVARIANTS
)


class TestMemoryTiers(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_memory_file = Path(self.temp_dir.name) / "test_memory.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_foundational_invariants_seeding(self):
        """Verifies that the 3 foundational bedrock invariants are seeded by default."""
        mem = load_memory(memory_path=self.temp_memory_file, auto_seed=True)
        entries = mem["entries"]

        self.assertGreaterEqual(len(entries), 3)
        titles = {e["title"] for e in entries}
        self.assertIn("Empirical Grounding", titles)
        self.assertIn("Epistemic Friction", titles)
        self.assertIn("Boundary Separation", titles)

        for e in entries:
            if e["title"] in ("Empirical Grounding", "Epistemic Friction", "Boundary Separation"):
                self.assertEqual(e["tier"], "skeleton")
                self.assertEqual(e["mutability"], "protected")
                self.assertEqual(e["author"], "consensus")

    def test_record_creation_tiers(self):
        """Tests creating skeleton vs adaptive memory entries."""
        # Adaptive entry
        entry_ad, _ = record_entry(
            title="Project Convention",
            content="Use snake_case for internal helper functions.",
            tags=["python", "style"],
            tier="adaptive",
            memory_path=self.temp_memory_file
        )
        self.assertEqual(entry_ad["tier"], "adaptive")
        self.assertEqual(entry_ad["mutability"], "mutable")
        self.assertEqual(entry_ad["version"], 1)

        # Skeleton entry
        entry_sk, _ = record_entry(
            title="Falsifiability Invariant",
            content="Every architectural claim must accompany a reproducible test case.",
            tags=["invariant", "testing"],
            tier="skeleton",
            memory_path=self.temp_memory_file
        )
        self.assertEqual(entry_sk["tier"], "skeleton")
        self.assertEqual(entry_sk["mutability"], "protected")
        self.assertEqual(entry_sk["version"], 1)

    def test_skeleton_protection_barrier_mutation(self):
        """Verifies that mutating a protected skeleton entry without --force-skeleton raises PermissionError."""
        record_entry(
            title="Core Architectural Boundary",
            content="Never bypass auth layer directly in workers.",
            tier="skeleton",
            memory_path=self.temp_memory_file
        )

        # Attempt mutation without force_skeleton -> must fail
        with self.assertRaises(PermissionError) as ctx:
            record_entry(
                title="Core Architectural Boundary",
                content="Attempted hostile override.",
                force_skeleton=False,
                memory_path=self.temp_memory_file
            )
        self.assertIn("Safety Violation", str(ctx.exception))
        self.assertIn("--force-skeleton", str(ctx.exception))

        # Mutation with force_skeleton -> must succeed
        updated_entry, _ = record_entry(
            title="Core Architectural Boundary",
            content="Authorized update with boundary notes.",
            force_skeleton=True,
            memory_path=self.temp_memory_file
        )
        self.assertEqual(updated_entry["content"], "Authorized update with boundary notes.")
        self.assertEqual(updated_entry["version"], 2)

    def test_skeleton_protection_barrier_deletion(self):
        """Verifies that deleting a protected skeleton entry without --force-skeleton raises PermissionError."""
        entry_sk, _ = record_entry(
            title="Protected Rule",
            content="Critical security invariant.",
            tier="skeleton",
            memory_path=self.temp_memory_file
        )
        entry_id = entry_sk["id"]

        # Delete without force_skeleton -> must fail
        with self.assertRaises(PermissionError) as ctx:
            delete_entry(entry_id, force_skeleton=False, memory_path=self.temp_memory_file)
        self.assertIn("Safety Violation", str(ctx.exception))
        self.assertIn("--force-skeleton", str(ctx.exception))

        # Delete with force_skeleton -> must succeed
        success = delete_entry(entry_id, force_skeleton=True, memory_path=self.temp_memory_file)
        self.assertTrue(success)

        # Confirm entry is gone
        mem = load_memory(memory_path=self.temp_memory_file, auto_seed=False)
        self.assertFalse(any(e["id"] == entry_id for e in mem["entries"]))

    def test_generous_append_adaptive(self):
        """Verifies generous append behavior for adaptive memory (version bump and tag merging)."""
        # Initial creation
        e1, _ = record_entry(
            title="Cache Expiration Standard",
            content="TTL set to 300 seconds for user profiles.",
            tags=["cache", "redis"],
            tier="adaptive",
            memory_path=self.temp_memory_file
        )
        self.assertEqual(e1["version"], 1)
        self.assertEqual(set(e1["tags"]), {"cache", "redis"})

        # Update with new content and additional tag
        e2, _ = record_entry(
            title="Cache Expiration Standard",
            content="TTL updated to 600 seconds with jitter.",
            tags=["performance", "jitter"],
            tier="adaptive",
            memory_path=self.temp_memory_file
        )
        self.assertEqual(e2["version"], 2)
        self.assertEqual(e2["content"], "TTL updated to 600 seconds with jitter.")
        # Tags should be merged (union)
        self.assertEqual(set(e2["tags"]), {"cache", "redis", "performance", "jitter"})

    def test_search_and_tier_filtering(self):
        """Verifies search filtering by tier (skeleton vs adaptive)."""
        record_entry("DB Replica Policy", "Read queries route to follower.", tier="skeleton", memory_path=self.temp_memory_file)
        record_entry("DB Index Naming", "Indexes use idx_table_col convention.", tier="adaptive", memory_path=self.temp_memory_file)

        skeleton_matches = search_entries("DB", tier_filter="skeleton", memory_path=self.temp_memory_file)
        adaptive_matches = search_entries("DB", tier_filter="adaptive", memory_path=self.temp_memory_file)

        self.assertTrue(all(e["tier"] == "skeleton" for e in skeleton_matches))
        self.assertTrue(any(e["title"] == "DB Replica Policy" for e in skeleton_matches))

        self.assertTrue(all(e["tier"] == "adaptive" for e in adaptive_matches))
        self.assertTrue(any(e["title"] == "DB Index Naming" for e in adaptive_matches))

    def test_backward_compatibility_migration(self):
        """Verifies seamless auto-migration of legacy memory files missing tier/version fields."""
        legacy_data = {
            "entries": [
                {
                    "id": "leg-101",
                    "project": "legacy-app",
                    "title": "Old Architectural Decision",
                    "content": "Use JWT for session validation.",
                    "tags": ["auth", "jwt"],
                    "created_at": "2026-01-01T00:00:00Z"
                }
            ]
        }
        with open(self.temp_memory_file, "w", encoding="utf-8") as f:
            json.dump(legacy_data, f)

        mem = load_memory(memory_path=self.temp_memory_file, auto_seed=False)
        migrated = mem["entries"][0]

        self.assertEqual(migrated["tier"], "adaptive")
        self.assertEqual(migrated["mutability"], "mutable")
        self.assertEqual(migrated["version"], 1)
        self.assertEqual(migrated["author"], "agent")
        self.assertEqual(migrated["title"], "Old Architectural Decision")


if __name__ == "__main__":
    unittest.main(verbosity=2)
