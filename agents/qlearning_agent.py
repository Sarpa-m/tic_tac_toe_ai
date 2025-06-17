import json
import random
from game.tic_tac_toe import TicTacToe
from tqdm import tqdm


class QLearningAgent:
    """
    Agente Q-Learning para o Jogo da Velha.
    Mantém uma tabela Q em arquivo JSON para persistência e continuidade do treinamento.
    """

    def __init__(
        self,
        alpha: float = 0.5,
        gamma: float = 0.9,
        epsilon: float = 1,
        epsilon_decay: float = 0.995,
        min_epsilon: float = 0.01,
        q_table_file: str = 'q_table.json'
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.q_table_file = q_table_file
        self.q_table = {}  # {state_key: {action: q_value}}
        self._load_q_table()

    def _state_key(self, state: tuple) -> str:
        return ''.join([s if s is not None else '-' for s in state])

    def get_q(self, state: tuple, action: int) -> float:
        key = self._state_key(state)
        if key not in self.q_table:
            self.q_table[key] = {}
        return self.q_table[key].get(str(action), 0.0)

    def choose_action(self, state: tuple, available_moves: list) -> int:
        if random.random() < self.epsilon:
            return random.choice(available_moves)
        q_values = {move: self.get_q(state, move) for move in available_moves}
        max_q = max(q_values.values())
        best_moves = [move for move, q in q_values.items() if q == max_q]
        return random.choice(best_moves)

    def update_q(
        self,
        state: tuple,
        action: int,
        reward: float,
        next_state: tuple,
        next_moves: list
    ):
        key = self._state_key(state)
        if key not in self.q_table:
            self.q_table[key] = {}
        old_q = self.q_table[key].get(str(action), 0.0)
        future_q = 0.0
        if next_moves:
            future_q = max(self.get_q(next_state, a) for a in next_moves)
        new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
        self.q_table[key][str(action)] = new_q

    def _load_q_table(self):
        try:
            with open(self.q_table_file, 'r') as f:
                self.q_table = json.load(f)
        except FileNotFoundError:
            self.q_table = {}

    def save_q_table(self):
        with open(self.q_table_file, 'w') as f:
            json.dump(self.q_table, f, indent=2)


