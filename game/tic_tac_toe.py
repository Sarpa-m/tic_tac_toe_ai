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
        """
        Reinicia o tabuleiro para o estado vazio.
        """
        # Lista de 9 elementos, todos None
        self.board = [None] * 9

    def get_available_moves(self):
        """
        Retorna uma lista de índices (0-8) de posições vazias no tabuleiro.
        """
        return [i for i, val in enumerate(self.board) if val is None]

    def make_move(self, position, player):
        """
        Marca a posição `position` (0 a 8) com o símbolo `player` ('X' ou 'O').
        Lança ValueError se o movimento for inválido.
        """
        if position < 0 or position > 8:
            raise ValueError(f"Posição inválida: {position}. Deve estar entre 0 e 8.")
        if player not in ('X', 'O'):
            raise ValueError(f"Jogador inválido: {player}. Deve ser 'X' ou 'O'.")
        if self.board[position] is not None:
            raise ValueError(f"Movimento inválido: posição {position} já está ocupada.")
        self.board[position] = player

    def check_winner(self):
        """
        Verifica o estado do jogo:
          - Retorna 'X' se o X venceu;
          - Retorna 'O' se o O venceu;
          - Retorna 'Draw' se todas as casas estão preenchidas e não há vencedor;
          - Retorna None se o jogo ainda não acabou.
        """
        # Combinações vencedoras
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
            (0, 4, 8), (2, 4, 6)              # diagonais
        ]
        for i, j, k in wins:
            if self.board[i] and self.board[i] == self.board[j] == self.board[k]:
                return self.board[i]

        if all(cell is not None for cell in self.board):
            return 'Draw'

        return None

    def get_state(self):
        """
        Retorna uma representação serializável do tabuleiro.
        Por exemplo, uma tupla de 9 elementos: ('X', None, 'O', ...)
        """
        return tuple(self.board)

    def __str__(self):
        """
        Impressão do tabuleiro em formato legível.
        """
        symbols = [val if val is not None else ' ' for val in self.board]
        rows = [symbols[0:3], symbols[3:6], symbols[6:9]]
        lines = [' | '.join(row) for row in rows]
        return '\n---------\n'.join(lines)
