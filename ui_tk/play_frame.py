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

        # --- Variáveis de Estado ---
        self.game = None
        self.player_types = {}
        self.agents = {}
        self.current_symbol = 'X'
        self.is_running = False  # Controla se uma sequência de jogos está ativa

        # --- Variáveis da UI ---
        self.player_x_var = tk.StringVar(value=self.PLAYER_OPTIONS[0])
        self.player_o_var = tk.StringVar(value=self.PLAYER_OPTIONS[1])
        self.games_to_play_var = tk.IntVar(value=1)
        self.delay_var = tk.IntVar(value=500)
        self.score_x = tk.IntVar(value=0)
        self.score_o = tk.IntVar(value=0)
        self.draws = tk.IntVar(value=0)
        
        # --- Configuração da UI ---
        self._setup_fonts()
        self._setup_ui_layout()

    def _setup_fonts(self):
        self.btn_font = font.Font(family="Helvetica", size=32, weight="bold")
        ttk.Style().configure("Victory.TButton", font=self.btn_font, padding=20, background="#90EE90")
        ttk.Style().configure("Board.TButton", font=self.btn_font, padding=20)

    def _setup_ui_layout(self):
        self._create_controls_frame()
        self._create_status_frame()
        self._create_board_frame()

    def _create_controls_frame(self):
        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(side="top", fill="x", pady=10, padx=10)

        # Seletor Jogador X
        tk.Label(self.controls_frame, text="Jogador X:").grid(row=0, column=0)
        self.p_x_menu = ttk.Combobox(self.controls_frame, textvariable=self.player_x_var, values=self.PLAYER_OPTIONS, state="readonly", width=12)
        self.p_x_menu.grid(row=0, column=1, padx=5)

        # Seletor Jogador O
        tk.Label(self.controls_frame, text="Jogador O:").grid(row=0, column=2)
        self.p_o_menu = ttk.Combobox(self.controls_frame, textvariable=self.player_o_var, values=self.PLAYER_OPTIONS, state="readonly", width=12)
        self.p_o_menu.grid(row=0, column=3, padx=5)

        # Seletor Nº de Jogos
        tk.Label(self.controls_frame, text="Nº de Jogos:").grid(row=0, column=4, padx=(15, 0))
        self.num_games_spinbox = ttk.Spinbox(self.controls_frame, from_=1, to=10000, textvariable=self.games_to_play_var, width=8)
        self.num_games_spinbox.grid(row=0, column=5, padx=(0, 10))

        # Seletor de Velocidade
        tk.Label(self.controls_frame, text="Velocidade (ms):").grid(row=0, column=6)
        self.delay_scale = tk.Scale(self.controls_frame, variable=self.delay_var, from_=50, to=2000, orient="horizontal", length=150)
        self.delay_scale.grid(row=0, column=7, padx=5)

        # Botões de Ação
        self.start_button = ttk.Button(self.controls_frame, text="Iniciar Sequência", command=self.start_sequence)
        self.start_button.grid(row=0, column=8, padx=10)
        ttk.Button(self.controls_frame, text="Voltar", command=self.controller.show_menu).grid(row=0, column=9, padx=10)

    def _create_status_frame(self):
        status_container = tk.Frame(self)
        status_container.pack(pady=10, fill="x")
        self.status_label = tk.Label(status_container, text="Selecione os jogadores e inicie a sequência.", font=("Helvetica", 16))
        self.status_label.pack()

        score_frame = tk.Frame(self)
        score_frame.pack(pady=5)
        tk.Label(score_frame, text="Vitórias X:").grid(row=0, column=0)
        tk.Label(score_frame, textvariable=self.score_x).grid(row=0, column=1, padx=5)
        tk.Label(score_frame, text="Vitórias O:").grid(row=0, column=2, padx=(10, 0))
        tk.Label(score_frame, textvariable=self.score_o).grid(row=0, column=3, padx=5)
        tk.Label(score_frame, text="Empates:").grid(row=0, column=4, padx=(10, 0))
        tk.Label(score_frame, textvariable=self.draws).grid(row=0, column=5, padx=5)
        ttk.Button(score_frame, text="Zerar Placar", command=self._reset_scores).grid(row=0, column=6, padx=20)

    def _create_board_frame(self):
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.buttons = []
        for r in range(3):
            self.board_frame.rowconfigure(r, weight=1)
            self.board_frame.columnconfigure(r, weight=1)
            row_buttons = []
            for c in range(3):
                btn = ttk.Button(self.board_frame, text=" ", style="Board.TButton",
                                 command=lambda rr=r, cc=c: self.on_human_move(rr, cc))
                btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    # --- LÓGICA DE CONTROLE DE JOGO (REATORADA) ---

    def start_sequence(self):
        if self.is_running:
            return
            
        self.is_running = True
        self._toggle_controls_state(tk.DISABLED)
        self._reset_scores()
        
        self.player_types = {'X': self.player_x_var.get(), 'O': self.player_o_var.get()}
        self._initialize_agents()
        
        self._start_new_game()

    def _start_new_game(self):
        self.game = TicTacToe()
        self.current_symbol = 'X'
        self._clear_board()
        
        current_game_num = self.score_x.get() + self.score_o.get() + self.draws.get() + 1
        total_games = self.games_to_play_var.get()
        self.status_label.config(text=f"Jogo {current_game_num} de {total_games}")
        
        self.after(50, self._game_loop) # Pequeno delay para iniciar o loop

    def _game_loop(self):
        if not self.is_running:
            return

        winner = self.game.check_winner()
        if winner:
            self.after(self.delay_var.get(), lambda: self._handle_game_over(winner))
            return

        if self.player_types[self.current_symbol] == "Human":
            self._enable_available_cells()
        else: # É a vez de uma IA
            self.after(self.delay_var.get(), self._make_ai_move)

    def _make_ai_move(self):
        move = self._get_ai_move(self.game, self.current_symbol)
        self._apply_move(move)
        
        self._game_loop() # Continua para o próximo turno

    def on_human_move(self, row, col):
        self._disable_all_cells()
        move = row * 3 + col
        self._apply_move(move)
        
        self._game_loop() # Continua para o próximo turno

    def _apply_move(self, move):
        # Aplica a jogada na lógica e na UI
        r, c = divmod(move, 3)
        self.buttons[r][c].config(text=self.current_symbol)
        self.game.make_move(move, self.current_symbol)
        self.current_symbol = 'O' if self.current_symbol == 'X' else 'X'

    def _handle_game_over(self, winner):
        self._update_score_and_board(winner)
        
        total_games_played = self.score_x.get() + self.score_o.get() + self.draws.get()
        total_games_to_play = self.games_to_play_var.get()
        
        if total_games_played < total_games_to_play:
            # Pausa para mostrar o resultado antes de começar o próximo jogo
            self.after(1500, self._start_new_game)
        else:
            self.status_label.config(text=f"Sequência concluída! Placar final: X {self.score_x.get()} - O {self.score_o.get()} - Empates {self.draws.get()}")
            self.is_running = False
            self._toggle_controls_state(tk.NORMAL)

    # --- MÉTODOS AUXILIARES ---

    def _initialize_agents(self):
        for symbol in ('X', 'O'):
            ptype = self.player_types.get(symbol)
            if ptype == 'Minimax':
                self.agents[symbol] = MinimaxAgent(ai_player=symbol, human_player='O' if symbol == 'X' else 'X')
            elif ptype == 'Q-Learning':
                self.agents[symbol] = QLearningAgent(0.5, 0.9, .01, 0.995, 0.01, f'q_table.json')
            else:
                self.agents[symbol] = None

    def _get_ai_move(self, game, symbol):
        ptype = self.player_types[symbol]
        if ptype == 'Random':
            return random.choice(game.get_available_moves())
        
        agent = self.agents[symbol]
        state = game.get_state()
        if ptype == 'Minimax':
            return agent.find_best_move(game)
        elif ptype == 'Q-Learning':
            return agent.choose_action(state, game.get_available_moves())
        return None

    def _update_score_and_board(self, winner):
        if winner == 'Draw':
            self.status_label.config(text="Empate!")
            self.draws.set(self.draws.get() + 1)
        else:
            self.status_label.config(text=f"Vitória de {winner}!")
            if winner == 'X':
                self.score_x.set(self.score_x.get() + 1)
            else:
                self.score_o.set(self.score_o.get() + 1)
            
            # Destaca a linha vencedora
            for pos in self.game.get_winning_line():
                r, c = divmod(pos, 3)
                self.buttons[r][c].config(style="Victory.TButton")

    def _clear_board(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=" ", style="Board.TButton", state=tk.DISABLED)

    def _enable_available_cells(self):
        for pos in self.game.get_available_moves():
            r, c = divmod(pos, 3)
            self.buttons[r][c].config(state=tk.NORMAL)

    def _disable_all_cells(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def _reset_scores(self):
        self.score_x.set(0)
        self.score_o.set(0)
        self.draws.set(0)

    def _toggle_controls_state(self, state):
        self.p_x_menu.config(state=state)
        self.p_o_menu.config(state=state)
        self.num_games_spinbox.config(state=state)
        self.delay_scale.config(state=state)
        self.start_button.config(state=state)