class TicTacToe:
    """
    Classe que representa o estado e as regras do jogo da velha (3x3).
    As células são armazenadas em uma lista de 9 posições:
      0 | 1 | 2
      3 | 4 | 5
      6 | 7 | 8
    Valores possíveis: 'X', 'O' ou None para vazio.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia o tabuleiro para o estado vazio."""
        self.board = [None] * 9

    def get_available_moves(self):
        """Retorna uma lista de índices (0-8) de posições vazias no tabuleiro."""
        return [i for i, val in enumerate(self.board) if val is None]

    def make_move(self, position, player):
        """Marca a posição com o símbolo do jogador ('X' ou 'O')."""
        if position < 0 or position > 8:
            raise ValueError(f"Posição inválida: {position}. Deve estar entre 0 e 8.")
        if player not in ('X', 'O'):
            raise ValueError(f"Jogador inválido: {player}. Deve ser 'X' ou 'O'.")
        if self.board[position] is not None:
            raise ValueError(f"Movimento inválido: posição {position} já está ocupada.")
        self.board[position] = player

    def check_winner(self):
        """Verifica o estado do jogo."""
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
            (0, 4, 8), (2, 4, 6)              # diagonais
        ]
        for i, j, k in wins:
            if self.board[i] and self.board[i] == self.board[j] == self.board[k]:
                return self.board[i]

        if self.is_full():
            return 'Draw'

        return None

    def get_winning_line(self):
        """Retorna a linha vencedora (lista de posições) ou [] se empate."""
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            a, b, c = line
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] is not None:
                return line
        return [] if self.is_full() else None

    def is_full(self):
        """Retorna True se o tabuleiro estiver completo."""
        return all(cell is not None for cell in self.board)

    def get_state(self):
        """Retorna o estado atual do tabuleiro como uma tupla."""
        return tuple(self.board)

    def __str__(self):
        """Retorna o tabuleiro como uma string legível."""
        symbols = [val if val is not None else ' ' for val in self.board]
        rows = [symbols[0:3], symbols[3:6], symbols[6:9]]
        lines = [' | '.join(row) for row in rows]
        return '\n---------\n'.join(lines)
