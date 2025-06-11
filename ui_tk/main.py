# ui_tk/main.py
import tkinter as tk
from .menu_frame import MenuFrame
#from .train_frame import TrainFrame
from .play_frame import PlayFrame  # crie esse arquivo com a classe PlayFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe AI")
        self.geometry("800x600")

        # Container que vai 'empilhar' os frames
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Instancia todos os frames e guarda em um dicionário
        self.frames = {}
        for F in (MenuFrame, PlayFrame):
            # Para TrainFrame e PlayFrame, estamos usando construtor sem parâmetros adicionais
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Exibe o menu inicialmente
        self.show_frame(MenuFrame)
        self.show_frame(PlayFrame)

    def show_frame(self, frame_class):
        """Traz o frame para frente."""
        frame = self.frames[frame_class]
        frame.tkraise()

    # Métodos chamados pelos botões em MenuFrame
    def show_menu(self):
        self.show_frame(MenuFrame)

    def show_play(self):
        self.show_frame(PlayFrame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
