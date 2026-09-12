#!/usr/bin/env python3
"""
Antigravity Autopilot - Standalone Desktop HUD (Dual-Mode GUI)

Features:
- Dual Form Factor: Compact floating sidebar (380px) expandable to full dashboard (840px).
- Zero External Dependencies: Pure Python standard library (tkinter + ttk).
- Real-Time Live Watcher: Automatically updates metrics whenever a new prompt is submitted.
- Interactive Prompt Sandbox: Test-type prompts to preview Q and Z in real time.
- Selectable Analysis Views: Cognitive Vector (Z), Viability (Q), Memory, Vocabulary, Stream.
- Windowless execution via pythonw.
"""

import os
import sys
import json
import time
import math
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from bin.cognitive_engine import CognitiveEngine, evaluate_prompt_viability, tokenize_words
from bin.agy_memory import load_memory
from bin.sync_transcript_learning import find_latest_transcript, clean_user_prompt

import tkinter as tk
from tkinter import ttk, messagebox

# UI Color Palette (Modern Dark Theme)
BG_MAIN = "#121214"
BG_PANEL = "#18181b"
BG_CARD = "#222226"
BG_CARD_HOVER = "#27272a"
BORDER_COLOR = "#3f3f46"
TEXT_PRIMARY = "#f4f4f5"
TEXT_MUTED = "#a1a1aa"
TEXT_DIM = "#71717a"

COLOR_GREEN = "#22c55e"
COLOR_CYAN = "#06b6d4"
COLOR_PURPLE = "#a855f7"
COLOR_AMBER = "#f59e0b"
COLOR_RED = "#ef4444"
COLOR_BLUE = "#3b82f6"

SIDEBAR_WIDTH = 380
SIDEBAR_HEIGHT = 680
DASHBOARD_WIDTH = 880
DASHBOARD_HEIGHT = 700


class AutopilotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Antigravity Autopilot HUD")
        self.root.geometry(f"{SIDEBAR_WIDTH}x{SIDEBAR_HEIGHT}")
        self.root.minsize(360, 600)
        self.root.configure(bg=BG_MAIN)

        self.engine = CognitiveEngine()
        self.is_expanded = False
        self.is_topmost = False
        self.last_step_index = -1
        self.last_transcript_path: Optional[Path] = None
        self.last_prompt_text = ""
        self.running = True

        self._setup_styles()
        self._build_ui()
        self._load_initial_state()

        # Start live watcher thread
        self.watcher_thread = threading.Thread(target=self._live_watcher_loop, daemon=True)
        self.watcher_thread.start()

        # Window protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(".", background=BG_PANEL, foreground=TEXT_PRIMARY, font=("Segoe UI", 9))
        style.configure("TFrame", background=BG_PANEL)
        style.configure("Card.TFrame", background=BG_CARD)
        
        # Notebook / Tabs
        style.configure("TNotebook", background=BG_PANEL, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_CARD, foreground=TEXT_MUTED, padding=[10, 5], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", BG_PANEL)],
                  foreground=[("selected", COLOR_CYAN)])

        # Treeview
        style.configure("Treeview",
                        background=BG_CARD,
                        foreground=TEXT_PRIMARY,
                        fieldbackground=BG_CARD,
                        borderwidth=0,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background=BG_PANEL,
                        foreground=COLOR_CYAN,
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#374151")])

    def _build_ui(self):
        # Container frame
        self.main_container = tk.Frame(self.root, bg=BG_MAIN)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Left Column: The Core Sidebar HUD (Always Visible)
        self.sidebar_frame = tk.Frame(self.main_container, bg=BG_PANEL, width=SIDEBAR_WIDTH)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sidebar_frame.pack_propagate(False)

        self._build_sidebar_header()
        self._build_sidebar_cognitive()
        self._build_sidebar_viability()
        self._build_sidebar_prompt_card()
        self._build_sidebar_memory_badge()
        self._build_sidebar_footer()

        # Right Column: Expanded Dashboard (Hidden by default)
        self.dashboard_frame = tk.Frame(self.main_container, bg=BG_MAIN)

    def _build_sidebar_header(self):
        header = tk.Frame(self.sidebar_frame, bg=BG_PANEL, height=45)
        header.pack(fill=tk.X, padx=12, pady=(10, 6))

        # Title and Live dot
        title_box = tk.Frame(header, bg=BG_PANEL)
        title_box.pack(side=tk.LEFT)

        self.live_indicator = tk.Label(title_box, text="●", font=("Segoe UI", 12), fg=COLOR_GREEN, bg=BG_PANEL)
        self.live_indicator.pack(side=tk.LEFT, padx=(0, 6))

        title_lbl = tk.Label(title_box, text="AUTOPILOT HUD", font=("Segoe UI", 11, "bold"), fg=TEXT_PRIMARY, bg=BG_PANEL)
        title_lbl.pack(side=tk.LEFT)

        # Action buttons on the right
        btn_box = tk.Frame(header, bg=BG_PANEL)
        btn_box.pack(side=tk.RIGHT)

        self.topmost_btn = tk.Button(btn_box, text="📌 Pin", font=("Segoe UI", 8),
                                     bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_CARD_HOVER,
                                     activeforeground=TEXT_PRIMARY, relief=tk.FLAT, bd=0, padx=6, pady=2,
                                     command=self._toggle_topmost)
        self.topmost_btn.pack(side=tk.LEFT, padx=3)

        self.expand_btn = tk.Button(btn_box, text="Expand ⤢", font=("Segoe UI", 8, "bold"),
                                    bg=BG_CARD, fg=COLOR_CYAN, activebackground=BG_CARD_HOVER,
                                    activeforeground=COLOR_CYAN, relief=tk.FLAT, bd=0, padx=6, pady=2,
                                    command=self._toggle_expand)
        self.expand_btn.pack(side=tk.LEFT, padx=3)

    def _build_sidebar_cognitive(self):
        card = tk.Frame(self.sidebar_frame, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill=tk.X, padx=12, pady=5)

        title_row = tk.Frame(card, bg=BG_CARD)
        title_row.pack(fill=tk.X, padx=10, pady=(8, 4))
        tk.Label(title_row, text="COGNITIVE VECTOR", font=("Segoe UI", 8, "bold"), fg=COLOR_CYAN, bg=BG_CARD).pack(side=tk.LEFT)
        self.lbl_z_vector = tk.Label(title_row, text="Z = 2.20 + 1.00i", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        self.lbl_z_vector.pack(side=tk.RIGHT)

        # Physical Action Depth (X)
        x_frame = tk.Frame(card, bg=BG_CARD)
        x_frame.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(x_frame, text="Action Depth (X):", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT)
        self.lbl_x_val = tk.Label(x_frame, text="2.20 / 3.0", font=("Segoe UI", 8, "bold"), fg=COLOR_GREEN, bg=BG_CARD)
        self.lbl_x_val.pack(side=tk.RIGHT)

        self.canvas_x = tk.Canvas(card, height=8, bg="#2d3748", highlightthickness=0)
        self.canvas_x.pack(fill=tk.X, padx=10, pady=(1, 6))

        # Epistemic Reflection (Y)
        y_frame = tk.Frame(card, bg=BG_CARD)
        y_frame.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(y_frame, text="Reflection Depth (Y):", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT)
        self.lbl_y_val = tk.Label(y_frame, text="1.00 / 3.0", font=("Segoe UI", 8, "bold"), fg=COLOR_PURPLE, bg=BG_CARD)
        self.lbl_y_val.pack(side=tk.RIGHT)

        self.canvas_y = tk.Canvas(card, height=8, bg="#2d3748", highlightthickness=0)
        self.canvas_y.pack(fill=tk.X, padx=10, pady=(1, 6))

        # Polar Metrics (R and Theta)
        polar_row = tk.Frame(card, bg=BG_CARD)
        polar_row.pack(fill=tk.X, padx=10, pady=(2, 8))
        self.lbl_polar = tk.Label(polar_row, text="R = 2.41 | θ = 24.5° (Balanced)", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD)
        self.lbl_polar.pack(side=tk.LEFT)

    def _build_sidebar_viability(self):
        card = tk.Frame(self.sidebar_frame, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill=tk.X, padx=12, pady=5)

        title_row = tk.Frame(card, bg=BG_CARD)
        title_row.pack(fill=tk.X, padx=10, pady=(8, 4))
        tk.Label(title_row, text="PROMPT VIABILITY", font=("Segoe UI", 8, "bold"), fg=COLOR_GREEN, bg=BG_CARD).pack(side=tk.LEFT)
        self.lbl_q_badge = tk.Label(title_row, text="Q = 0.85 (High)", font=("Segoe UI", 9, "bold"), fg=COLOR_GREEN, bg=BG_CARD)
        self.lbl_q_badge.pack(side=tk.RIGHT)

        self.canvas_q = tk.Canvas(card, height=8, bg="#2d3748", highlightthickness=0)
        self.canvas_q.pack(fill=tk.X, padx=10, pady=(2, 6))

        # Subscore pills
        pills_row = tk.Frame(card, bg=BG_CARD)
        pills_row.pack(fill=tk.X, padx=10, pady=(2, 8))
        self.lbl_sub_spec = tk.Label(pills_row, text="Spec: 0.85", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD)
        self.lbl_sub_spec.pack(side=tk.LEFT, padx=(0, 8))
        self.lbl_sub_test = tk.Label(pills_row, text="Test: 0.80", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD)
        self.lbl_sub_test.pack(side=tk.LEFT, padx=(0, 8))
        self.lbl_sub_scope = tk.Label(pills_row, text="Scope: 0.90", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD)
        self.lbl_sub_scope.pack(side=tk.LEFT)

    def _build_sidebar_prompt_card(self):
        card = tk.Frame(self.sidebar_frame, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=12, pady=5)

        title_row = tk.Frame(card, bg=BG_CARD)
        title_row.pack(fill=tk.X, padx=10, pady=(8, 2))
        tk.Label(title_row, text="LATEST INGESTED PROMPT", font=("Segoe UI", 8, "bold"), fg=COLOR_AMBER, bg=BG_CARD).pack(side=tk.LEFT)

        self.txt_prompt_snippet = tk.Text(card, bg=BG_PANEL, fg=TEXT_PRIMARY, font=("Consolas", 8),
                                          height=4, wrap=tk.WORD, bd=0, highlightthickness=0, padx=6, pady=4)
        self.txt_prompt_snippet.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        self.txt_prompt_snippet.insert(tk.END, "Waiting for prompt input...")
        self.txt_prompt_snippet.configure(state=tk.DISABLED)

        # 1-Line Refinement Advice Box
        self.advice_frame = tk.Frame(card, bg=BG_CARD)
        self.advice_frame.pack(fill=tk.X, padx=10, pady=(2, 8))
        self.lbl_advice_title = tk.Label(self.advice_frame, text="💡 Tip:", font=("Segoe UI", 8, "bold"), fg=COLOR_AMBER, bg=BG_CARD)
        self.lbl_advice_title.pack(side=tk.LEFT)
        self.lbl_advice_text = tk.Label(self.advice_frame, text="Prompt is well-formed.", font=("Segoe UI", 8),
                                        fg=TEXT_MUTED, bg=BG_CARD, wraplength=270, justify=tk.LEFT)
        self.lbl_advice_text.pack(side=tk.LEFT, padx=4)

    def _build_sidebar_memory_badge(self):
        card = tk.Frame(self.sidebar_frame, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill=tk.X, padx=12, pady=5)

        row = tk.Frame(card, bg=BG_CARD)
        row.pack(fill=tk.X, padx=10, pady=6)
        tk.Label(row, text="EPISTEMIC MEMORY:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT)
        self.lbl_memory_counts = tk.Label(row, text="3 Skeleton | 1 Adaptive", font=("Segoe UI", 8, "bold"), fg=COLOR_BLUE, bg=BG_CARD)
        self.lbl_memory_counts.pack(side=tk.RIGHT)

    def _build_sidebar_footer(self):
        footer = tk.Frame(self.sidebar_frame, bg=BG_PANEL, height=35)
        footer.pack(fill=tk.X, padx=12, pady=(4, 10))

        self.lbl_status = tk.Label(footer, text="Live watching...", font=("Segoe UI", 8), fg=TEXT_DIM, bg=BG_PANEL)
        self.lbl_status.pack(side=tk.LEFT)

        btn_refresh = tk.Button(footer, text="🔄 Sync", font=("Segoe UI", 8),
                                bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_CARD_HOVER,
                                activeforeground=TEXT_PRIMARY, relief=tk.FLAT, bd=0, padx=6, pady=2,
                                command=self._manual_refresh)
        btn_refresh.pack(side=tk.RIGHT)

    def _build_dashboard_panel(self):
        # Build multi-tab notebook
        self.notebook = ttk.Notebook(self.dashboard_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Live Prompt Sandbox
        self.tab_sandbox = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_sandbox, text="🎯 Prompt Sandbox")
        self._build_tab_sandbox()

        # Tab 2: Cognitive State Deep Dive
        self.tab_cognitive = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_cognitive, text="🧠 Complex Vector Z")
        self._build_tab_cognitive()

        # Tab 3: Epistemic Memory
        self.tab_memory = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_memory, text="⚓ Epistemic Memory")
        self._build_tab_memory()

        # Tab 4: Dynamically Learned Vocabulary
        self.tab_vocab = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_vocab, text="📊 Dynamic Vocabulary")
        self._build_tab_vocab()

        # Tab 5: Trajectory Event Stream
        self.tab_stream = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_stream, text="📡 Telemetry Stream")
        self._build_tab_stream()

    def _build_tab_sandbox(self):
        frame = self.tab_sandbox
        tk.Label(frame, text="Interactive Prompt Evaluator", font=("Segoe UI", 11, "bold"), fg=COLOR_CYAN, bg=BG_PANEL).pack(anchor=tk.W, padx=12, pady=(10, 2))
        tk.Label(frame, text="Type or paste any prompt draft below to preview its Cognitive Vector (Z), Viability Score (Q), and advice live.",
                 font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor=tk.W, padx=12, pady=(0, 8))

        self.sandbox_input = tk.Text(frame, bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                                     font=("Consolas", 10), height=7, wrap=tk.WORD, bd=0, highlightthickness=1,
                                     highlightbackground=BORDER_COLOR, padx=8, pady=8)
        self.sandbox_input.pack(fill=tk.X, padx=12, pady=4)
        self.sandbox_input.insert(tk.END, "Implement websocket reconnect logic and write comprehensive unit tests with exit code 0.")

        btn_row = tk.Frame(frame, bg=BG_PANEL)
        btn_row.pack(fill=tk.X, padx=12, pady=6)
        btn_eval = tk.Button(btn_row, text="⚡ Evaluate Prompt", font=("Segoe UI", 9, "bold"),
                             bg=COLOR_CYAN, fg="#000000", activebackground="#22d3ee", relief=tk.FLAT, bd=0, padx=12, pady=4,
                             command=self._evaluate_sandbox_prompt)
        btn_eval.pack(side=tk.LEFT)

        # Output Card
        self.sandbox_output_frame = tk.Frame(frame, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.sandbox_output_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(6, 12))

        self.lbl_sandbox_results = tk.Label(self.sandbox_output_frame, text="", font=("Segoe UI", 9), fg=TEXT_PRIMARY,
                                            bg=BG_CARD, justify=tk.LEFT, anchor=tk.NW, padx=12, pady=12)
        self.lbl_sandbox_results.pack(fill=tk.BOTH, expand=True)

    def _build_tab_cognitive(self):
        frame = self.tab_cognitive
        tk.Label(frame, text="Continuous Cognitive Plane Mathematics (Z = X + iY)", font=("Segoe UI", 11, "bold"), fg=COLOR_PURPLE, bg=BG_PANEL).pack(anchor=tk.W, padx=12, pady=(10, 4))
        
        info_text = (
            "Under Project Autopilot, execution and reflection depth are modeled as a complex state:\n\n"
            "• Physical Action Depth (X = Re(Z) ∈ [1.0, 3.0]):\n"
            "    X = 1.0 : Single-pass batch implementation without secondary audit.\n"
            "    X = 2.2 : Resilient Double-Pass Gold Standard (Pass 1 batch + Pass 2 gap audit + delta check).\n"
            "    X = 3.0 : Triple-pass multi-tier adversarial stress testing and edge-case validation.\n\n"
            "• Epistemic Reflection Depth (Y = Im(Z) ∈ [0.0, 3.0]):\n"
            "    Internal verification tokens, proof-checking, counterfactual simulation, and test synthesis.\n\n"
            "• Polar Dynamics (Z = R * exp(iθ)):\n"
            "    R = sqrt(X^2 + Y^2) : Total Attentional Energy budget allocated to prompt.\n"
            "    θ = arctan(Y/X)     : Attentional Phase Angle (<20° Action-Dominant, >55° Epistemic-Dominant)."
        )
        txt = tk.Label(frame, text=info_text, font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL, justify=tk.LEFT, padx=12, pady=8)
        txt.pack(anchor=tk.W)

    def _build_tab_memory(self):
        frame = self.tab_memory
        top_row = tk.Frame(frame, bg=BG_PANEL)
        top_row.pack(fill=tk.X, padx=12, pady=(10, 6))

        tk.Label(top_row, text="Dual-Tier Epistemic Memory", font=("Segoe UI", 11, "bold"), fg=COLOR_BLUE, bg=BG_PANEL).pack(side=tk.LEFT)

        columns = ("id", "tier", "title", "version", "tags")
        self.tree_memory = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        self.tree_memory.heading("id", text="ID")
        self.tree_memory.heading("tier", text="Tier")
        self.tree_memory.heading("title", text="Title")
        self.tree_memory.heading("version", text="Ver")
        self.tree_memory.heading("tags", text="Tags")

        self.tree_memory.column("id", width=70)
        self.tree_memory.column("tier", width=90)
        self.tree_memory.column("title", width=220)
        self.tree_memory.column("version", width=45)
        self.tree_memory.column("tags", width=180)

        self.tree_memory.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

    def _build_tab_vocab(self):
        frame = self.tab_vocab
        tk.Label(frame, text="Dynamically Learned Subword Feature Hashing (Online SGD)", font=("Segoe UI", 11, "bold"), fg=COLOR_GREEN, bg=BG_PANEL).pack(anchor=tk.W, padx=12, pady=(10, 6))

        columns = ("token", "delta_x", "delta_y", "count", "category")
        self.tree_vocab = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        self.tree_vocab.heading("token", text="Subword / Token")
        self.tree_vocab.heading("delta_x", text="ΔX (Action)")
        self.tree_vocab.heading("delta_y", text="ΔY (Reflection)")
        self.tree_vocab.heading("count", text="Observed")
        self.tree_vocab.heading("category", text="Category")

        self.tree_vocab.column("token", width=140)
        self.tree_vocab.column("delta_x", width=90)
        self.tree_vocab.column("delta_y", width=100)
        self.tree_vocab.column("count", width=70)
        self.tree_vocab.column("category", width=160)

        self.tree_vocab.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

    def _build_tab_stream(self):
        frame = self.tab_stream
        tk.Label(frame, text="Recent Telemetry Trajectories (Local Samples)", font=("Segoe UI", 11, "bold"), fg=COLOR_AMBER, bg=BG_PANEL).pack(anchor=tk.W, padx=12, pady=(10, 6))

        columns = ("time", "prompt", "target_x", "target_y", "q")
        self.tree_stream = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        self.tree_stream.heading("time", text="Timestamp")
        self.tree_stream.heading("prompt", text="Prompt Snippet")
        self.tree_stream.heading("target_x", text="Target X*")
        self.tree_stream.heading("target_y", text="Target Y*")
        self.tree_stream.heading("q", text="Viability Q")

        self.tree_stream.column("time", width=130)
        self.tree_stream.column("prompt", width=260)
        self.tree_stream.column("target_x", width=70)
        self.tree_stream.column("target_y", width=70)
        self.tree_stream.column("q", width=80)

        self.tree_stream.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

    def _toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        if self.is_topmost:
            self.topmost_btn.configure(text="📌 Pinned", fg=COLOR_GREEN)
        else:
            self.topmost_btn.configure(text="📌 Pin", fg=TEXT_MUTED)

    def _toggle_expand(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            if not hasattr(self, "notebook"):
                self._build_dashboard_panel()
            self.sidebar_frame.pack_configure(expand=False)
            self.dashboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.root.geometry(f"{DASHBOARD_WIDTH}x{DASHBOARD_HEIGHT}")
            self.expand_btn.configure(text="Compact ⤡")
            self._populate_dashboard_tables()
            self._evaluate_sandbox_prompt()
        else:
            self.dashboard_frame.pack_forget()
            self.sidebar_frame.pack_configure(expand=True)
            self.root.geometry(f"{SIDEBAR_WIDTH}x{SIDEBAR_HEIGHT}")
            self.expand_btn.configure(text="Expand ⤢")

    def _draw_progress_bar(self, canvas: tk.Canvas, frac: float, color: str):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1:
            width = 280
        if height <= 1:
            height = 8

        fill_width = max(2, int(width * max(0.0, min(1.0, frac))))
        canvas.create_rectangle(0, 0, width, height, fill="#27272a", width=0)
        canvas.create_rectangle(0, 0, fill_width, height, fill=color, width=0)

    def _load_initial_state(self):
        # Baseline engine state
        pred = self.engine.predict("Initial baseline evaluation")
        viability = evaluate_prompt_viability("Initial baseline evaluation")
        self._render_metrics(self.last_prompt_text or "Engine active. Ready for user prompts.", pred, viability)
        self._update_memory_counts()

    def _update_memory_counts(self):
        try:
            mem = load_memory()
            records = mem.get("records", [])
            sk = sum(1 for r in records if r.get("tier") == "skeleton")
            ad = sum(1 for r in records if r.get("tier", "adaptive") != "skeleton")
            self.lbl_memory_counts.configure(text=f"{sk} Skeleton | {ad} Adaptive")
        except Exception:
            pass

    def _render_metrics(self, prompt: str, pred: Dict[str, Any], viability: Dict[str, Any]):
        # Update Z
        x = pred.get("recommended_x", 2.2)
        y = pred.get("reflection_depth", 1.0)
        r = pred.get("energy_radius", math.sqrt(x*x + y*y))
        theta = pred.get("phase_angle_deg", math.degrees(math.atan2(y, x)))

        self.lbl_z_vector.configure(text=f"Z = {x:.2f} + {y:.2f}i")
        self.lbl_x_val.configure(text=f"{x:.2f} / 3.0")
        self.lbl_y_val.configure(text=f"{y:.2f} / 3.0")

        # Color based on flow
        if theta < 20.0:
            flow = "Action-Dominant"
            flow_color = COLOR_GREEN
        elif theta > 55.0:
            flow = "Epistemic-Dominant"
            flow_color = COLOR_PURPLE
        else:
            flow = "Balanced Flow"
            flow_color = COLOR_CYAN

        self.lbl_polar.configure(text=f"R = {r:.2f} | θ = {theta:.1f}° ({flow})", fg=flow_color)

        # Draw progress bars
        self.root.update_idletasks()
        self._draw_progress_bar(self.canvas_x, (x - 1.0) / 2.0, COLOR_GREEN)
        self._draw_progress_bar(self.canvas_y, y / 3.0, COLOR_PURPLE)

        # Update Q
        q = viability.get("overall_score", 0.8)
        q_label = viability.get("viability_label", "Moderate")
        q_color = COLOR_GREEN if q >= 0.78 else (COLOR_AMBER if q >= 0.55 else COLOR_RED)

        self.lbl_q_badge.configure(text=f"Q = {q:.2f} ({q_label})", fg=q_color)
        self._draw_progress_bar(self.canvas_q, q, q_color)

        subs = viability.get("sub_scores", {})
        self.lbl_sub_spec.configure(text=f"Spec: {subs.get('specificity', 0.5):.2f}")
        self.lbl_sub_test.configure(text=f"Test: {subs.get('verifiability', 0.5):.2f}")
        self.lbl_sub_scope.configure(text=f"Scope: {subs.get('scope_density', 0.5):.2f}")

        # Update Prompt Snippet
        self.txt_prompt_snippet.configure(state=tk.NORMAL)
        self.txt_prompt_snippet.delete("1.0", tk.END)
        snippet = prompt.strip().replace("\n", " ")
        if len(snippet) > 140:
            snippet = snippet[:140] + "..."
        self.txt_prompt_snippet.insert(tk.END, snippet)
        self.txt_prompt_snippet.configure(state=tk.DISABLED)

        # Advice
        hint = viability.get("refinement_hint")
        if hint and q < 0.78:
            self.lbl_advice_title.configure(text="💡 Tip:", fg=COLOR_AMBER)
            self.lbl_advice_text.configure(text=hint, fg=COLOR_AMBER)
        else:
            self.lbl_advice_title.configure(text="✓ Status:", fg=COLOR_GREEN)
            self.lbl_advice_text.configure(text="Prompt is clear & well-anchored.", fg=COLOR_GREEN)

        self._update_memory_counts()
        self.lbl_status.configure(text=f"Updated: {datetime.now().strftime('%H:%M:%S')}")

    def _populate_dashboard_tables(self):
        # Populate Memory
        for item in self.tree_memory.get_children():
            self.tree_memory.delete(item)
        try:
            mem = load_memory()
            for r in mem.get("records", []):
                self.tree_memory.insert("", tk.END, values=(
                    r.get("id"),
                    r.get("tier", "adaptive").upper(),
                    r.get("title"),
                    f"v{r.get('version', 1)}",
                    ", ".join(r.get("tags", []))
                ))
        except Exception:
            pass

        # Populate Vocab
        for item in self.tree_vocab.get_children():
            self.tree_vocab.delete(item)
        try:
            tokens = self.engine.weights.get("token_frequencies", {})
            for tok, cnt in sorted(tokens.items(), key=lambda x: x[1], reverse=True)[:40]:
                h = self.engine._hash_token(tok)
                dx = self.engine.weights.get("weights_x", [0.0]*256)[h]
                dy = self.engine.weights.get("weights_y", [0.0]*256)[h]
                self.tree_vocab.insert("", tk.END, values=(
                    tok,
                    f"{dx:+.3f}",
                    f"{dy:+.3f}",
                    cnt,
                    "Dynamic Token"
                ))
        except Exception:
            pass

        # Populate Stream
        for item in self.tree_stream.get_children():
            self.tree_stream.delete(item)
        try:
            samples_path = Path.home() / ".gemini" / "autopilot" / "telemetry" / "samples.jsonl"
            if samples_path.exists():
                with open(samples_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for l in reversed(lines[-25:]):
                    try:
                        d = json.loads(l)
                        p_snip = d.get("prompt_snippet", "")[:45]
                        self.tree_stream.insert("", tk.END, values=(
                            d.get("timestamp", "")[:19],
                            p_snip,
                            f"{d.get('target_x', 0):.2f}",
                            f"{d.get('target_y', 0):.2f}",
                            f"{d.get('viability_score', 0):.2f}"
                        ))
                    except Exception:
                        pass
        except Exception:
            pass

    def _evaluate_sandbox_prompt(self):
        text = self.sandbox_input.get("1.0", tk.END).strip()
        if not text:
            return
        pred = self.engine.predict(text)
        viab = evaluate_prompt_viability(text)

        x = pred.get("recommended_x", 2.2)
        y = pred.get("reflection_depth", 1.0)
        q = viab.get("overall_score", 0.8)
        subs = viab.get("sub_scores", {})
        hint = viab.get("refinement_hint", "None")
        ex = viab.get("example_rewrite", "None")

        res = (
            f"🎯 PROMPT VIABILITY: Q = {q:.2f} ({viab.get('viability_label', 'Unknown')})\n"
            f"   • Specificity  : {subs.get('specificity', 0):.2f}\n"
            f"   • Verifiability: {subs.get('verifiability', 0):.2f}\n"
            f"   • Scope Density: {subs.get('scope_density', 0):.2f}\n\n"
            f"🧠 COGNITIVE STATE : Z = {x:.2f} + {y:.2f}i (Passes: {x:.1f}, Phase: {pred.get('phase_angle_deg', 0):.1f}°)\n"
            f"💡 REFINEMENT ADVICE:\n   {hint}\n\n"
            f"📝 EXAMPLE REWRITE:\n   {ex}"
        )
        self.lbl_sandbox_results.configure(text=res)

    def _live_watcher_loop(self):
        """Continuously watches active transcript.jsonl for new prompt turns."""
        while self.running:
            try:
                transcript_path = find_latest_transcript()
                if transcript_path and transcript_path.exists():
                    self.last_transcript_path = transcript_path
                    self._check_transcript_updates(transcript_path)
            except Exception:
                pass
            time.sleep(0.75)

    def _check_transcript_updates(self, transcript_path: Path):
        try:
            with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            # Look for newest USER_INPUT from the bottom
            for idx in range(len(lines) - 1, -1, -1):
                line = lines[idx].strip()
                if not line:
                    continue
                try:
                    step = json.loads(line)
                    step_type = step.get("type")
                    if step_type == "USER_INPUT":
                        step_idx = step.get("step_index", idx)
                        if step_idx != self.last_step_index:
                            content = step.get("content", "")
                            cleaned = clean_user_prompt(content)
                            if cleaned and cleaned != self.last_prompt_text:
                                self.last_step_index = step_idx
                                self.last_prompt_text = cleaned
                                # Schedule UI update on main thread
                                self.root.after(0, self._on_new_prompt_detected, cleaned)
                        break
                except Exception:
                    pass
        except Exception:
            pass

    def _on_new_prompt_detected(self, prompt: str):
        pred = self.engine.predict(prompt)
        viab = evaluate_prompt_viability(prompt)
        self._render_metrics(prompt, pred, viab)
        if self.is_expanded:
            self._populate_dashboard_tables()

    def _manual_refresh(self):
        self.engine = CognitiveEngine()
        if self.last_prompt_text:
            self._on_new_prompt_detected(self.last_prompt_text)
        else:
            self._load_initial_state()
        if self.is_expanded:
            self._populate_dashboard_tables()

    def _on_close(self):
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AutopilotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
