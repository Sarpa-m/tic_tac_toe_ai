import tkinter as tk
from tkinter import ttk

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        """
        parent     – janela principal (App)
        controller – instância de App, precisa ter métodos show_train() e show_play()
        """
        super().__init__(parent)
        self.controller = controller

        # Título
        title = ttk.Label(self, text="Tic-Tac-Toe AI", font=("Helvetica", 24))
        title.pack(pady=40)

        # Botão Treinar
        btn_train = ttk.Button(
            self, text="Treinar Agente",
            command=self.controller.show_train
        )
        btn_train.pack(pady=10, ipadx=10, ipady=5)

        # Botão Jogar
        btn_play = ttk.Button(
            self, text="Jogar",
            command=self.controller.show_play
        )
        btn_play.pack(pady=10, ipadx=10, ipady=5)

        # Opcional: Botão Sair
        btn_exit = ttk.Button(
            self, text="Sair",
            command=self.controller.quit
        )
        btn_exit.pack(pady=30, ipadx=10, ipady=5)
