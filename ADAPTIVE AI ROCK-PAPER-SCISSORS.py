import tkinter as tk
from tkinter import messagebox
import random
from collections import Counter, deque

# ============================================================
# ADAPTIVE AI ROCK PAPER SCISSORS - PREMIUM DASHBOARD
# ============================================================
# AI concepts:
#   - Intelligent Agent
#   - Agent and Environment
#   - Adversarial Search / Minimax
#   - Player behavior prediction
#   - Adaptive difficulty
#
# FAIR-PLAY:
# The AI chooses its move BEFORE the current player move is
# added to history. Therefore it cannot see the current move
# and then choose a counter.
# ============================================================

MOVES = ["Rock", "Paper", "Scissors"]

COUNTER = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock"
}

BEATS = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}

EMOJI = {
    "Rock": "✊",
    "Paper": "✋",
    "Scissors": "✌"
}

def payoff(ai_move, player_move):
    if ai_move == player_move:
        return 0
    if COUNTER[player_move] == ai_move:
        return 1
    return -1


class AdaptiveRPSAI:
    def __init__(self):
        self.player_history = []
        self.ai_history = []
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        self.difficulty = "Medium"

    def predict_player_move(self):
        if not self.player_history:
            return random.choice(MOVES)

        counts = Counter(self.player_history)
        recent = self.player_history[-6:]
        recent_counts = Counter(recent)

        scores = {}
        for move in MOVES:
            scores[move] = counts[move] + (2 * recent_counts[move])

        highest = max(scores.values())
        candidates = [m for m in MOVES if scores[m] == highest]
        return random.choice(candidates)

    # One-step minimax for the 3-state adversarial game.
    def minimax(self, predicted_player_move):
        best_score = -999
        best_moves = []

        for ai_move in MOVES:
            score = payoff(ai_move, predicted_player_move)

            if score > best_score:
                best_score = score
                best_moves = [ai_move]
            elif score == best_score:
                best_moves.append(ai_move)

        return random.choice(best_moves)

    def update_difficulty(self):
        total = self.player_score + self.ai_score

        if total < 4:
            self.difficulty = "Medium"
            return

        player_rate = self.player_score / total

        if player_rate >= 0.65:
            self.difficulty = "Hard"
        elif player_rate <= 0.35:
            self.difficulty = "Easy"
        else:
            self.difficulty = "Medium"

    def choose_move(self):
        predicted = self.predict_player_move()
        optimal = self.minimax(predicted)

        probabilities = {
            "Easy": 0.35,
            "Medium": 0.60,
            "Hard": 0.80
        }

        if random.random() < probabilities[self.difficulty]:
            return optimal

        return random.choice(MOVES)

    def learn(self, player_move, ai_move):
        self.player_history.append(player_move)
        self.ai_history.append(ai_move)

        result = payoff(ai_move, player_move)

        if result == 1:
            self.ai_score += 1
        elif result == -1:
            self.player_score += 1
        else:
            self.draws += 1

        self.update_difficulty()

    def reset(self):
        self.player_history.clear()
        self.ai_history.clear()
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        self.difficulty = "Medium"


class PremiumRPSDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS AI • Adaptive Rock Paper Scissors")
        self.root.geometry("1250x820")
        self.root.minsize(1050, 720)
        self.root.configure(bg="#07111f")

        self.ai = AdaptiveRPSAI()
        self.round_number = 0
        self.last_result = "READY"
        self.history_rows = deque(maxlen=8)

        self.colors = {
            "bg": "#07111f",
            "panel": "#0d1b2e",
            "panel2": "#10243a",
            "border": "#1e3a56",
            "cyan": "#38d9ff",
            "blue": "#4f7cff",
            "purple": "#9b6cff",
            "green": "#2ee6a6",
            "red": "#ff5f73",
            "yellow": "#ffd166",
            "white": "#f4f8ff",
            "muted": "#8298b2",
            "dark_text": "#06101c"
        }

        self.setup_fonts()
        self.build_ui()
        self.animate_header()
        self.animate_ai_core()

    def setup_fonts(self):
        self.font_family = "Segoe UI"

    def label(self, parent, text="", size=10, weight="normal",
              fg=None, bg=None, **kwargs):
        return tk.Label(
            parent,
            text=text,
            font=(self.font_family, size, weight),
            fg=fg or self.colors["white"],
            bg=bg or self.colors["panel"],
            **kwargs
        )

    def rounded_panel(self, parent, bg=None, padx=1, pady=1):
        return tk.Frame(
            parent,
            bg=bg or self.colors["panel"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=padx,
            pady=pady
        )

    def build_ui(self):
        self.build_topbar()

        body = tk.Frame(self.root, bg=self.colors["bg"])
        body.pack(fill="both", expand=True, padx=28, pady=(5, 22))

        self.build_left_dashboard(body)
        self.build_center_game(body)
        self.build_right_intelligence(body)

        self.build_bottom_status()

    # ---------------- TOP BAR ----------------

    def build_topbar(self):
        top = tk.Frame(self.root, bg=self.colors["bg"])
        top.pack(fill="x", padx=30, pady=(22, 8))

        left = tk.Frame(top, bg=self.colors["bg"])
        left.pack(side="left")

        self.logo_canvas = tk.Canvas(
            left, width=48, height=48,
            bg=self.colors["bg"], highlightthickness=0
        )
        self.logo_canvas.pack(side="left", padx=(0, 12))
        self.logo_canvas.create_oval(
            5, 5, 43, 43,
            outline=self.colors["cyan"],
            width=2
        )
        self.logo_canvas.create_text(
            24, 24, text="AI",
            fill=self.colors["cyan"],
            font=(self.font_family, 11, "bold")
        )

        title_frame = tk.Frame(left, bg=self.colors["bg"])
        title_frame.pack(side="left")

        self.label(
            title_frame,
            "NEXUS AI",
            23, "bold",
            self.colors["white"],
            self.colors["bg"]
        ).pack(anchor="w")

        self.label(
            title_frame,
            "ADAPTIVE ROCK • PAPER • SCISSORS",
            9, "bold",
            self.colors["cyan"],
            self.colors["bg"]
        ).pack(anchor="w")

        right = tk.Frame(top, bg=self.colors["bg"])
        right.pack(side="right")

        self.live_dot = tk.Canvas(
            right, width=14, height=14,
            bg=self.colors["bg"], highlightthickness=0
        )
        self.live_dot.pack(side="left", padx=(0, 5))
        self.live_circle = self.live_dot.create_oval(
            3, 3, 11, 11, fill=self.colors["green"], outline=""
        )

        self.label(
            right,
            "AI SYSTEM ONLINE",
            9, "bold",
            self.colors["green"],
            self.colors["bg"]
        ).pack(side="left")

    # ---------------- LEFT DASHBOARD ----------------

    def build_left_dashboard(self, body):
        left = tk.Frame(body, bg=self.colors["bg"], width=240)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        self.make_section_title(left, "LIVE SCOREBOARD")

        self.player_card = self.make_metric_card(
            left, "YOU", "0", self.colors["cyan"]
        )
        self.ai_card = self.make_metric_card(
            left, "AI", "0", self.colors["purple"]
        )
        self.draw_card = self.make_metric_card(
            left, "DRAWS", "0", self.colors["yellow"]
        )

        self.make_section_title(left, "PERFORMANCE")

        perf = self.rounded_panel(left, self.colors["panel"])
        perf.pack(fill="x", pady=(0, 12))

        self.win_rate_label = self.label(
            perf, "0%", 25, "bold",
            self.colors["green"], self.colors["panel"]
        )
        self.win_rate_label.pack(pady=(15, 0))

        self.label(
            perf, "YOUR WIN RATE", 8, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(pady=(2, 12))

        self.difficulty_box = self.rounded_panel(
            left, self.colors["panel"]
        )
        self.difficulty_box.pack(fill="x", pady=(0, 12))

        self.label(
            self.difficulty_box,
            "CURRENT MODE",
            8, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(pady=(13, 2))

        self.difficulty_label = self.label(
            self.difficulty_box,
            "● MEDIUM",
            15, "bold",
            self.colors["yellow"], self.colors["panel"]
        )
        self.difficulty_label.pack(pady=(0, 13))

        self.reset_btn = self.make_button(
            left, "↻  NEW GAME",
            self.reset_game,
            self.colors["panel2"],
            self.colors["white"]
        )
        self.reset_btn.pack(fill="x", pady=(5, 0))

    def make_section_title(self, parent, text):
        frame = tk.Frame(parent, bg=self.colors["bg"])
        frame.pack(fill="x", pady=(5, 8))

        self.label(
            frame, text, 9, "bold",
            self.colors["muted"], self.colors["bg"]
        ).pack(anchor="w")

    def make_metric_card(self, parent, title, value, accent):
        card = self.rounded_panel(parent, self.colors["panel"])
        card.pack(fill="x", pady=(0, 8))

        line = tk.Frame(card, bg=accent, width=4)
        line.pack(side="left", fill="y")

        content = tk.Frame(card, bg=self.colors["panel"])
        content.pack(fill="both", expand=True, padx=12, pady=8)

        self.label(
            content, title, 8, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(anchor="w")

        value_label = self.label(
            content, value, 22, "bold",
            accent, self.colors["panel"]
        )
        value_label.pack(anchor="w")

        return value_label

    # ---------------- CENTER GAME ----------------

    def build_center_game(self, body):
        center = tk.Frame(body, bg=self.colors["bg"])
        center.pack(side="left", fill="both", expand=True, padx=12)

        hero = self.rounded_panel(center, self.colors["panel"])
        hero.pack(fill="x", pady=(0, 12))

        hero_top = tk.Frame(hero, bg=self.colors["panel"])
        hero_top.pack(fill="x", padx=20, pady=(15, 0))

        self.round_label = self.label(
            hero_top, "ROUND 01", 9, "bold",
            self.colors["cyan"], self.colors["panel"]
        )
        self.round_label.pack(side="left")

        self.result_badge = self.label(
            hero_top, "● READY", 9, "bold",
            self.colors["yellow"], self.colors["panel"]
        )
        self.result_badge.pack(side="right")

        title = self.label(
            hero,
            "MAKE YOUR MOVE",
            24, "bold",
            self.colors["white"], self.colors["panel"]
        )
        title.pack(pady=(10, 0))

        subtitle = self.label(
            hero,
            "The AI predicts from previous rounds — never your current move.",
            9, "normal",
            self.colors["muted"], self.colors["panel"]
        )
        subtitle.pack(pady=(3, 18))

        arena = tk.Frame(hero, bg=self.colors["panel"])
        arena.pack(fill="x", padx=25, pady=(0, 22))

        self.player_display = self.make_choice_display(
            arena, "YOU", self.colors["cyan"]
        )
        self.player_display["frame"].pack(
            side="left", expand=True, fill="both", padx=(0, 8)
        )

        vs_frame = tk.Frame(arena, bg=self.colors["panel"], width=70)
        vs_frame.pack(side="left", fill="y")
        self.label(
            vs_frame, "VS", 14, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(expand=True)

        self.ai_display = self.make_choice_display(
            arena, "NEXUS AI", self.colors["purple"]
        )
        self.ai_display["frame"].pack(
            side="left", expand=True, fill="both", padx=(8, 0)
        )

        controls = tk.Frame(hero, bg=self.colors["panel"])
        controls.pack(pady=(0, 20))

        self.choice_buttons = []

        data = [
            ("✊", "ROCK", "Rock"),
            ("✋", "PAPER", "Paper"),
            ("✌", "SCISSORS", "Scissors")
        ]

        for icon, text, move in data:
            btn = self.make_choice_button(
                controls, icon, text, move
            )
            btn.pack(side="left", padx=5)
            self.choice_buttons.append(btn)

        self.result_label = self.label(
            hero,
            "Choose a move to begin the match",
            12, "bold",
            self.colors["muted"], self.colors["panel"]
        )
        self.result_label.pack(pady=(0, 20))

        self.build_recent_rounds(center)

    def make_choice_display(self, parent, title, accent):
        frame = tk.Frame(
            parent,
            bg=self.colors["panel2"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        self.label(
            frame, title, 8, "bold",
            self.colors["muted"], self.colors["panel2"]
        ).pack(pady=(12, 0))

        emoji_label = self.label(
            frame, "?", 42, "normal",
            accent, self.colors["panel2"]
        )
        emoji_label.pack(pady=(3, 0))

        move_label = self.label(
            frame, "WAITING", 9, "bold",
            self.colors["white"], self.colors["panel2"]
        )
        move_label.pack(pady=(0, 12))

        return {
            "frame": frame,
            "emoji": emoji_label,
            "move": move_label,
            "accent": accent
        }

    def make_choice_button(self, parent, icon, text, move):
        btn = tk.Button(
            parent,
            text=f"{icon}\n{text}",
            command=lambda m=move: self.play(m),
            font=(self.font_family, 11, "bold"),
            fg=self.colors["white"],
            bg=self.colors["panel2"],
            activeforeground=self.colors["dark_text"],
            activebackground=self.colors["cyan"],
            relief="flat",
            bd=0,
            width=10,
            height=3,
            cursor="hand2"
        )

        btn.bind("<Enter>", lambda e, b=btn: b.config(
            bg=self.colors["cyan"], fg=self.colors["dark_text"]
        ))
        btn.bind("<Leave>", lambda e, b=btn: b.config(
            bg=self.colors["panel2"], fg=self.colors["white"]
        ))

        return btn

    def build_recent_rounds(self, parent):
        panel = self.rounded_panel(parent, self.colors["panel"])
        panel.pack(fill="both", expand=True)

        header = tk.Frame(panel, bg=self.colors["panel"])
        header.pack(fill="x", padx=16, pady=(12, 7))

        self.label(
            header, "RECENT ROUNDS", 9, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(side="left")

        self.rounds_count_label = self.label(
            header, "0 rounds", 8, "bold",
            self.colors["cyan"], self.colors["panel"]
        )
        self.rounds_count_label.pack(side="right")

        self.history_frame = tk.Frame(panel, bg=self.colors["panel"])
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.empty_history = self.label(
            self.history_frame,
            "No rounds yet • Your match history will appear here",
            9, "normal",
            self.colors["muted"], self.colors["panel"]
        )
        self.empty_history.pack(expand=True)

    # ---------------- RIGHT AI PANEL ----------------

    def build_right_intelligence(self, body):
        right = tk.Frame(body, bg=self.colors["bg"], width=265)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        self.make_section_title(right, "AI INTELLIGENCE")

        core = self.rounded_panel(right, self.colors["panel"])
        core.pack(fill="x", pady=(0, 10))

        self.core_canvas = tk.Canvas(
            core,
            width=170,
            height=170,
            bg=self.colors["panel"],
            highlightthickness=0
        )
        self.core_canvas.pack(pady=(12, 2))

        self.core_canvas.create_oval(
            28, 28, 142, 142,
            outline=self.colors["border"],
            width=2
        )
        self.core_ring = self.core_canvas.create_arc(
            28, 28, 142, 142,
            start=20, extent=290,
            outline=self.colors["cyan"],
            width=4,
            style="arc"
        )
        self.core_canvas.create_text(
            85, 72,
            text="AI",
            fill=self.colors["white"],
            font=(self.font_family, 19, "bold")
        )
        self.core_text = self.core_canvas.create_text(
            85, 101,
            text="THINKING",
            fill=self.colors["cyan"],
            font=(self.font_family, 8, "bold")
        )

        self.label(
            core,
            "ADAPTIVE DECISION CORE",
            8, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(pady=(0, 12))

        self.make_section_title(right, "AI ANALYSIS")

        analysis = self.rounded_panel(right, self.colors["panel"])
        analysis.pack(fill="x", pady=(0, 10))

        self.prediction_value = self.make_analysis_row(
            analysis, "NEXT PREDICTION", "—"
        )
        self.strategy_value = self.make_analysis_row(
            analysis, "STRATEGY", "Balanced"
        )
        self.learning_value = self.make_analysis_row(
            analysis, "LEARNING", "0 moves"
        )

        self.make_section_title(right, "MOVE PATTERN")

        pattern = self.rounded_panel(right, self.colors["panel"])
        pattern.pack(fill="x", pady=(0, 10))

        self.pattern_labels = {}

        for move in MOVES:
            row = tk.Frame(pattern, bg=self.colors["panel"])
            row.pack(fill="x", padx=12, pady=5)

            self.label(
                row,
                f"{EMOJI[move]}  {move}",
                8, "bold",
                self.colors["white"], self.colors["panel"]
            ).pack(side="left")

            value = self.label(
                row, "0", 8, "bold",
                self.colors["cyan"], self.colors["panel"]
            )
            value.pack(side="right")
            self.pattern_labels[move] = value

        self.make_section_title(right, "FAIR PLAY")

        fair = self.rounded_panel(right, self.colors["panel"])
        fair.pack(fill="x")

        self.label(
            fair,
            "✓ CURRENT MOVE HIDDEN\n\n"
            "✓ NO LOOK-AHEAD CHEATING\n\n"
            "✓ USES PREVIOUS HISTORY\n\n"
            "✓ RANDOMNESS PRESERVED",
            8, "bold",
            self.colors["green"], self.colors["panel"],
            justify="left"
        ).pack(anchor="w", padx=13, pady=13)

    def make_analysis_row(self, parent, title, value):
        row = tk.Frame(parent, bg=self.colors["panel"])
        row.pack(fill="x", padx=12, pady=5)

        self.label(
            row, title, 7, "bold",
            self.colors["muted"], self.colors["panel"]
        ).pack(side="left")

        value_label = self.label(
            row, value, 8, "bold",
            self.colors["white"], self.colors["panel"]
        )
        value_label.pack(side="right")

        return value_label

    # ---------------- BOTTOM STATUS ----------------

    def build_bottom_status(self):
        bar = tk.Frame(
            self.root,
            bg=self.colors["panel2"],
            height=28
        )
        bar.pack(fill="x", side="bottom")

        self.status_text = self.label(
            bar,
            "● SYSTEM READY     •     MINIMAX ENGINE ACTIVE     •     FAIR-PLAY MODE",
            8, "bold",
            self.colors["green"], self.colors["panel2"]
        )
        self.status_text.pack(pady=7)

    # ---------------- GAME LOGIC ----------------

    def play(self, player_move):
        # The AI chooses BEFORE the current move is added to history.
        self.set_buttons_state("disabled")

        self.core_text = self.core_canvas.itemconfig(
            self.core_text, text="CALCULATING"
        )

        self.root.after(180, lambda: self.finish_play(player_move))

    def finish_play(self, player_move):
        ai_move = self.ai.choose_move()

        self.round_number += 1
        self.player_display["emoji"].config(text=EMOJI[player_move])
        self.player_display["move"].config(text=player_move.upper())

        self.ai_display["emoji"].config(text=EMOJI[ai_move])
        self.ai_display["move"].config(text=ai_move.upper())

        result = self.get_result(player_move, ai_move)

        self.ai.learn(player_move, ai_move)

        self.last_result = result
        self.update_dashboard(player_move, ai_move, result)
        self.add_history(player_move, ai_move, result)

        self.set_buttons_state("normal")

    def get_result(self, player, ai):
        if player == ai:
            return "DRAW"
        if COUNTER[player] == ai:
            return "AI WINS"
        return "YOU WIN"

    def update_dashboard(self, player, ai, result):
        self.round_label.config(text=f"ROUND {self.round_number:02d}")

        if result == "YOU WIN":
            result_color = self.colors["green"]
            result_text = "● VICTORY"
        elif result == "AI WINS":
            result_color = self.colors["red"]
            result_text = "● AI WINS"
        else:
            result_color = self.colors["yellow"]
            result_text = "● DRAW"

        self.result_badge.config(
            text=result_text, fg=result_color
        )
        self.result_label.config(
            text=self.get_result_message(result),
            fg=result_color
        )

        self.player_card.config(text=str(self.ai.player_score))
        self.ai_card.config(text=str(self.ai.ai_score))
        self.draw_card.config(text=str(self.ai.draws))

        total = self.ai.player_score + self.ai.ai_score
        rate = (
            (self.ai.player_score / total) * 100
            if total else 0
        )
        self.win_rate_label.config(text=f"{rate:.0f}%")

        difficulty_colors = {
            "Easy": self.colors["green"],
            "Medium": self.colors["yellow"],
            "Hard": self.colors["red"]
        }
        diff = self.ai.difficulty
        self.difficulty_label.config(
            text=f"● {diff.upper()}",
            fg=difficulty_colors[diff]
        )

        prediction = self.ai.predict_player_move()
        self.prediction_value.config(text=prediction.upper())
        self.strategy_value.config(
            text={
                "Easy": "SOFT",
                "Medium": "BALANCED",
                "Hard": "AGGRESSIVE"
            }[diff]
        )
        self.learning_value.config(
            text=f"{len(self.ai.player_history)} moves"
        )

        for move in MOVES:
            self.pattern_labels[move].config(
                text=str(self.ai.player_history.count(move))
            )

        self.rounds_count_label.config(
            text=f"{self.round_number} rounds"
        )

        self.status_text.config(
            text=(
                "● AI ADAPTED     •     "
                f"DIFFICULTY: {diff.upper()}     •     "
                "CURRENT MOVE WAS HIDDEN     •     "
                "MINIMAX ACTIVE"
            )
        )

    def get_result_message(self, result):
        if result == "YOU WIN":
            return "🎉 Excellent! You outplayed the AI."
        if result == "AI WINS":
            return "🤖 The AI got this round. Keep going!"
        return "⚖ Perfectly matched — a draw."

    def add_history(self, player, ai, result):
        if hasattr(self, "empty_history") and self.empty_history.winfo_exists():
            self.empty_history.destroy()

        for widget in self.history_frame.winfo_children():
            widget.destroy()

        self.history_rows.appendleft(
            (self.round_number, player, ai, result)
        )

        for number, p, a, r in self.history_rows:
            row = tk.Frame(
                self.history_frame,
                bg=self.colors["panel2"],
                height=28
            )
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            self.label(
                row, f"#{number:02d}", 8, "bold",
                self.colors["muted"], self.colors["panel2"],
                width=5
            ).pack(side="left")

            self.label(
                row, f"{EMOJI[p]} {p}", 8, "bold",
                self.colors["white"], self.colors["panel2"],
                width=13, anchor="w"
            ).pack(side="left")

            self.label(
                row, "VS", 7, "bold",
                self.colors["muted"], self.colors["panel2"],
                width=4
            ).pack(side="left")

            self.label(
                row, f"{EMOJI[a]} {a}", 8, "bold",
                self.colors["white"], self.colors["panel2"],
                width=13, anchor="w"
            ).pack(side="left")

            result_color = {
                "YOU WIN": self.colors["green"],
                "AI WINS": self.colors["red"],
                "DRAW": self.colors["yellow"]
            }[r]

            self.label(
                row, r, 7, "bold",
                result_color, self.colors["panel2"],
                width=10
            ).pack(side="right", padx=5)

    # ---------------- RESET ----------------

    def reset_game(self):
        answer = messagebox.askyesno(
            "New Game",
            "Reset the current match and AI learning history?"
        )

        if not answer:
            return

        self.ai.reset()
        self.round_number = 0
        self.last_result = "READY"
        self.history_rows.clear()

        self.player_card.config(text="0")
        self.ai_card.config(text="0")
        self.draw_card.config(text="0")
        self.win_rate_label.config(text="0%")
        self.difficulty_label.config(
            text="● MEDIUM",
            fg=self.colors["yellow"]
        )

        self.round_label.config(text="ROUND 01")
        self.result_badge.config(
            text="● READY",
            fg=self.colors["yellow"]
        )
        self.result_label.config(
            text="Choose a move to begin the match",
            fg=self.colors["muted"]
        )

        for display in [self.player_display, self.ai_display]:
            display["emoji"].config(text="?")
            display["move"].config(text="WAITING")

        self.prediction_value.config(text="—")
        self.strategy_value.config(text="Balanced")
        self.learning_value.config(text="0 moves")

        for move in MOVES:
            self.pattern_labels[move].config(text="0")

        for widget in self.history_frame.winfo_children():
            widget.destroy()

        self.empty_history = self.label(
            self.history_frame,
            "No rounds yet • Your match history will appear here",
            9, "normal",
            self.colors["muted"], self.colors["panel"]
        )
        self.empty_history.pack(expand=True)

        self.rounds_count_label.config(text="0 rounds")

        self.status_text.config(
            text="● SYSTEM READY     •     MINIMAX ENGINE ACTIVE     •     FAIR-PLAY MODE"
        )

    # ---------------- HELPERS ----------------

    def make_button(self, parent, text, command, bg, fg):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=(self.font_family, 9, "bold"),
            fg=fg,
            bg=bg,
            activeforeground=self.colors["dark_text"],
            activebackground=self.colors["cyan"],
            relief="flat",
            bd=0,
            padx=8,
            pady=10,
            cursor="hand2"
        )

        btn.bind("<Enter>", lambda e: btn.config(
            bg=self.colors["cyan"],
            fg=self.colors["dark_text"]
        ))
        btn.bind("<Leave>", lambda e: btn.config(
            bg=bg,
            fg=fg
        ))

        return btn

    def set_buttons_state(self, state):
        for btn in self.choice_buttons:
            btn.config(state=state)

    # ---------------- ANIMATION ----------------

    def animate_header(self):
        self.pulse = not getattr(self, "pulse", False)

        if self.pulse:
            self.live_dot.itemconfig(
                self.live_circle, fill=self.colors["green"]
            )
        else:
            self.live_dot.itemconfig(
                self.live_circle, fill="#126c55"
            )

        self.root.after(700, self.animate_header)

    def animate_ai_core(self):
        self.core_angle = getattr(self, "core_angle", 20)
        self.core_angle = (self.core_angle + 12) % 360

        self.core_canvas.itemconfig(
            self.core_ring,
            start=self.core_angle,
            extent=285
        )

        self.root.after(80, self.animate_ai_core)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumRPSDashboard(root)
    root.mainloop()
