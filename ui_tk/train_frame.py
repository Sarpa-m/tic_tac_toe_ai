# ui_tk/train_frame.py

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from training_manager import TrainingManager

class TrainFrame(tk.Frame):
    def __init__(self, parent, controller, episodes=5000, opponent='random', symbol='X'):
        """
        parent     – janela principal (App)
        controller – instância de App, usada para voltar ao menu
        episodes   – número total de episódios de treino
        opponent   – 'random' ou 'minimax'
        symbol     – 'X' ou 'O' (símbolo do agente Q-Learning)
        """
        super().__init__(parent)
        self.controller = controller
        self.episodes = episodes

        # Título
        ttk.Label(self, text="Treinamento Q-Learning", font=("Helvetica", 18))\
            .pack(pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=600, mode="determinate",
            maximum=self.episodes
        )
        self.progress.pack(pady=10)

        # Frame para o gráfico
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Evolução de Vitórias / Empates / Derrotas")
        self.ax.set_xlabel("Episódio")
        self.ax.set_ylabel("Quantidade")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        # Botão Voltar
        ttk.Button(
            self, text="Voltar ao Menu",
            command=self._on_back
        ).pack(pady=20)

        # Listas para armazenar histórico
        self.episodes_list = []
        self.wins_list = []
        self.draws_list = []
        self.losses_list = []

        # Inicia o gerador de treino
        manager = TrainingManager(
            num_episodes=self.episodes,
            opponent_type=opponent,
            agent_symbol=symbol
        )
        self.train_gen = manager.train_generator()

        # Começa o loop de atualização
        self._update()

    def _update(self):
        try:
            ep, w, d, l, eps = next(self.train_gen)
            # Atualiza barra
            self.progress['value'] = ep

            # Acumula histórico
            self.episodes_list.append(ep)
            self.wins_list.append(w)
            self.draws_list.append(d)
            self.losses_list.append(l)

            # Atualiza gráfico
            self.ax.clear()
            self.ax.plot(self.episodes_list, self.wins_list, label="Vitórias")
            self.ax.plot(self.episodes_list, self.draws_list, label="Empates")
            self.ax.plot(self.episodes_list, self.losses_list, label="Derrotas")
            self.ax.legend(loc="upper left")
            self.ax.set_xlim(0, self.episodes)
            self.ax.set_ylim(
                0,
                max(max(self.wins_list + self.draws_list + self.losses_list), 1)
            )
            self.ax.set_title(f"TREINO: Episódio {ep} / {self.episodes}  •  ε={eps:.4f}")
            self.ax.set_xlabel("Episódio")
            self.ax.set_ylabel("Contagem")
            self.canvas.draw()

            # Agenda próxima atualização em 10 ms
            self.after(10, self._update)

        except StopIteration:
            # Treino concluído
            ttk.Label(
                self, text="Treinamento concluído!",
                font=("Helvetica", 14)
            ).pack(pady=5)

    def _on_back(self):
        # parar o gerador se precisar (opcional)
        self.controller.show_menu()
