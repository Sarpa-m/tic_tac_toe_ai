import tkinter as tk
from tkinter import ttk, font
import random

from game.tic_tac_toe import TicTacToe
from agents.minimax_agent import MinimaxAgent
from agents.qlearning_agent import QLearningAgent


class PlayFrame(tk.Frame):
    PLAYER_OPTIONS = ["Human", "Minimax", "Q-Learning", "Random"]

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.delay = 500

        self._setup_fonts()
        self._setup_controls()
        self._setup_board()
        self._setup_status()
        self._reset_game_state()

    def _setup_fonts(self):
        self.btn_font = font.Font(family="Helvetica", size=32, weight="bold")
        ttk.Style().configure("Victory.TButton", font=self.btn_font, padding=20, background="lightgreen")

    def _setup_controls(self):
        controls = tk.Frame(self)
        controls.pack(side="top", fill="x", pady=10)

        self.player_x_var = self._create_player_selector(controls, "Player X:", 0)
        self.player_o_var = self._create_player_selector(controls, "Player O:", 2, default=1)

        tk.Label(controls, text="Delay (ms):").grid(row=0, column=4, padx=5)
        self.delay_scale = tk.Scale(controls, from_=100, to=2000, orient="horizontal",
                                     command=self._on_delay_change, length=200)
        self.delay_scale.set(self.delay)
        self.delay_scale.grid(row=0, column=5, padx=5)

        ttk.Button(controls, text="Start", command=self.start_game).grid(row=0, column=6, padx=10)
        ttk.Button(controls, text="Back", command=self.controller.show_menu).grid(row=0, column=7, padx=10)

    def _setup_status(self):
        self.status_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.status_label.pack(pady=10)

        self.score_frame = tk.Frame(self)
        self.score_frame.pack(pady=5)
        self.score_x = tk.IntVar(value=0)
        self.score_o = tk.IntVar(value=0)
        self.draws = tk.IntVar(value=0)

        tk.Label(self.score_frame, text="Vitórias X:").grid(row=0, column=0, padx=5)
        tk.Label(self.score_frame, textvariable=self.score_x).grid(row=0, column=1, padx=5)
        tk.Label(self.score_frame, text="Vitórias O:").grid(row=0, column=2, padx=5)
        tk.Label(self.score_frame, textvariable=self.score_o).grid(row=0, column=3, padx=5)
        tk.Label(self.score_frame, text="Empates:").grid(row=0, column=4, padx=5)
        tk.Label(self.score_frame, textvariable=self.draws).grid(row=0, column=5, padx=5)

    def _create_player_selector(self, parent, label, col, default=0):
        tk.Label(parent, text=label).grid(row=0, column=col, padx=5)
        var = tk.StringVar(value=self.PLAYER_OPTIONS[default])
        menu = ttk.Combobox(parent, textvariable=var, values=self.PLAYER_OPTIONS, state="readonly", width=12)
        menu.grid(row=0, column=col + 1, padx=5)
        return var

    def _setup_board(self):
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(fill="both", expand=True, padx=20, pady=20)

        for i in range(3):
            self.board_frame.rowconfigure(i, weight=1)
            self.board_frame.columnconfigure(i, weight=1)

        ttk.Style().configure("Board.TButton", font=self.btn_font, padding=20)

        self.buttons = [[self._create_board_button(r, c) for c in range(3)] for r in range(3)]

    def _create_board_button(self, r, c):
        btn = ttk.Button(self.board_frame, text=" ", style="Board.TButton",
                         command=lambda rr=r, cc=c: self.on_cell_clicked(rr, cc), state="disabled")
        btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
        return btn

    def _reset_game_state(self):
        self.game = None
        self.moves = []
        self.current_symbol = 'X'
        self.player_types = {}
        self.agents = {}

    def _on_delay_change(self, val):
        self.delay = int(val)

    def start_game(self):
        self._clear_board()
        self.status_label.config(text="")
        self._reset_game_state()

        self.game = TicTacToe()
        self.player_types = {'X': self.player_x_var.get(), 'O': self.player_o_var.get()}

        self._initialize_agents()

        if 'Human' not in self.player_types.values():
            self.moves = self.simulate_game()
            self.game = TicTacToe()
            self._replay_moves(0)
        else:
            self.next_turn()

    def _clear_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(text=" ", state="disabled", style="Board.TButton")

    def _initialize_agents(self):
        for symbol in ('X', 'O'):
            ptype = self.player_types[symbol]
            if ptype == 'Minimax':
                self.agents[symbol] = MinimaxAgent(ai_player=symbol, human_player='O' if symbol == 'X' else 'X')
            elif ptype == 'Q-Learning':
                self.agents[symbol] = QLearningAgent()
            else:
                self.agents[symbol] = None

    def simulate_game(self):
        sim = TicTacToe()
        moves, symbol = [], 'X'
        while True:
            move = self._get_ai_move(sim, symbol)
            sim.make_move(move, symbol)
            moves.append((move, symbol))
            if sim.check_winner():
                break
            symbol = 'O' if symbol == 'X' else 'X'
        return moves

    def _replay_moves(self, idx):
        if idx >= len(self.moves):
            self._end_game()
            return
        pos, symbol = self.moves[idx]
        self.game.make_move(pos, symbol)
        r, c = divmod(pos, 3)
        self.buttons[r][c].config(text=symbol)
        self.after(self.delay, lambda: self._replay_moves(idx + 1))

    def next_turn(self):
        if self.player_types[self.current_symbol] == 'Human':
            for pos in self.game.get_available_moves():
                r, c = divmod(pos, 3)
                self.buttons[r][c].config(state="normal")
        else:
            self.after(self.delay, self.ai_move)

    def on_cell_clicked(self, row, col):
        pos = row * 3 + col
        self.buttons[row][col].config(state="disabled")
        self._handle_move(pos)

    def ai_move(self):
        pos = self._get_ai_move(self.game, self.current_symbol)
        self._handle_move(pos)

    def _get_ai_move(self, game, symbol):
        ptype = self.player_types[symbol]
        if ptype == 'Random':
            return random.choice(game.get_available_moves())
        agent = self.agents[symbol]
        state = game.get_state()
        return agent.find_best_move(game) if isinstance(agent, MinimaxAgent) else agent.choose_action(state, game.get_available_moves())

    def _handle_move(self, pos):
        self.game.make_move(pos, self.current_symbol)
        r, c = divmod(pos, 3)
        self.buttons[r][c].config(text=self.current_symbol, state="disabled")

        if self.game.check_winner():
            self._end_game()
        else:
            self.current_symbol = 'O' if self.current_symbol == 'X' else 'X'
            self.next_turn()

    def _end_game(self):
        winner = self.game.check_winner()
        winning_line = self.game.get_winning_line()

        if winner == 'Draw':
            self.status_label.config(text="Empate!")
            self.draws.set(self.draws.get() + 1)
            for row in self.buttons:
                for btn in row:
                    btn.config(style="TButton")
        else:
            self.status_label.config(text=f"Vitória de {winner}!")
            if winner == 'X':
                self.score_x.set(self.score_x.get() + 1)
            elif winner == 'O':
                self.score_o.set(self.score_o.get() + 1)
            for pos in winning_line:
                r, c = divmod(pos, 3)
                self.buttons[r][c].config(style="Victory.TButton")
