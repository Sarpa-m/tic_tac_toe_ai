# ui_tk/main.py
import tkinter as tk
from .menu_frame import MenuFrame
# mais tarde importaremos também:
from .train_frame import TrainFrame
# from .play_frame  import PlayFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe AI")
        self.geometry("800x600")

        # inicializa frames
        self.menu = MenuFrame(self, self)
        self.train = TrainFrame(self, self)
        # self.play  = PlayFrame(self, self)

        # mostra o menu
        self.menu.pack(fill="both", expand=True)

    def show_menu(self):
        self._switch_frame(self.menu)

    def show_train(self):
        self._switch_frame(self.train)

    def show_play(self):
        self._switch_frame(self.play)

    def _switch_frame(self, frame):
        for child in self.winfo_children():
            child.pack_forget()
        frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
