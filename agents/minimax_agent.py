import math
from game.tic_tac_toe import TicTacToe


class MinimaxAgent:
    """
    Agente Minimax para o Jogo da Velha.
    Usa busca exaustiva para escolher o movimento ótimo, assumindo que o oponente joga de forma ótima.
    """

    def __init__(self, ai_player: str = 'X', human_player: str = 'O'):
        self.ai_player = ai_player
        self.human_player = human_player

    def evaluate(self, board: TicTacToe) -> int:
        """
        Avalia o estado terminal do tabuleiro:
          +10 se o agente AI venceu;
          -10 se o oponente venceu;
          0 se empate.
        Retorna None se o jogo não acabou.
        """
        result = board.check_winner()
        if result == self.ai_player:
            return 10
        elif result == self.human_player:
            return -10
        elif result == 'Draw':
            return 0
        return None

    def minimax(self, board: TicTacToe, depth: int, is_maximizing: bool) -> int:
        """
        Função recursiva Minimax.
        depth: profundidade atual da recursão (opcional para aprimoramentos).
        is_maximizing: True se for a vez do jogador maximizador (AI), False caso contrário.
        """
        score = self.evaluate(board)
        if score is not None:
            return score

        if is_maximizing:
            best_val = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.ai_player)
                val = self.minimax(board, depth + 1, False)
                board.board[move] = None  # desfaz movimento
                best_val = max(best_val, val)
            return best_val
        else:
            best_val = math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.human_player)
                val = self.minimax(board, depth + 1, True)
                board.board[move] = None  # desfaz movimento
                best_val = min(best_val, val)
            return best_val

    def find_best_move(self, board: TicTacToe) -> int:
        """
        Retorna o índice (0-8) do melhor movimento para o agente AI no tabuleiro atual.
        """
        best_move = None
        best_val = -math.inf
        for move in board.get_available_moves():
            board.make_move(move, self.ai_player)
            move_val = self.minimax(board, 0, False)
            board.board[move] = None  # desfaz movimento

            if move_val > best_val:
                best_val = move_val
                best_move = move

        return best_move
