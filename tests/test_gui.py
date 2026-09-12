#!/usr/bin/env python3
"""
Automated unit and component test for Antigravity Autopilot Desktop HUD (bin/agy_gui.py).
Runs headlessly by withdrawing the root window.
"""

import sys
import unittest
import tkinter as tk
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from bin.agy_gui import AutopilotGUI, SIDEBAR_WIDTH, DASHBOARD_WIDTH


class TestAutopilotGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create hidden root
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = AutopilotGUI(cls.root)
        cls.app.running = False  # Disable background thread loop in tests

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def test_gui_initial_state(self):
        """Verify initial sidebar layout, gauges, and title."""
        self.assertEqual(self.root.title(), "Antigravity Autopilot HUD")
        self.assertFalse(self.app.is_expanded)
        self.assertFalse(self.app.is_topmost)
        self.assertIsNotNone(self.app.lbl_z_vector)
        self.assertIsNotNone(self.app.lbl_q_badge)

    def test_metric_rendering(self):
        """Test rendering arbitrary Z and Q updates."""
        pred = {
            "recommended_x": 2.25,
            "reflection_depth": 1.15,
            "energy_radius": 2.52,
            "phase_angle_deg": 27.1
        }
        viability = {
            "overall_score": 0.91,
            "viability_label": "High",
            "sub_scores": {"specificity": 0.9, "verifiability": 0.9, "scope_density": 0.92},
            "refinement_hint": "None"
        }
        self.app._render_metrics("Test prompt execution", pred, viability)
        self.assertEqual(self.app.lbl_z_vector.cget("text"), "Z = 2.25 + 1.15i")
        self.assertIn("0.91", self.app.lbl_q_badge.cget("text"))

    def test_toggle_topmost(self):
        """Test toggling topmost pin."""
        initial = self.app.is_topmost
        self.app._toggle_topmost()
        self.assertEqual(self.app.is_topmost, not initial)
        self.app._toggle_topmost()
        self.assertEqual(self.app.is_topmost, initial)

    def test_toggle_expand_and_collapse(self):
        """Test expanding to multi-tab dashboard and collapsing back to sidebar."""
        self.assertFalse(self.app.is_expanded)
        self.app._toggle_expand()
        self.assertTrue(self.app.is_expanded)
        self.assertTrue(hasattr(self.app, "notebook"))
        self.assertEqual(len(self.app.notebook.tabs()), 6)

        # Collapse back
        self.app._toggle_expand()
        self.assertFalse(self.app.is_expanded)


if __name__ == "__main__":
    unittest.main()
