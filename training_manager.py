import os
import csv
import random
from tqdm import tqdm

from game.tic_tac_toe import TicTacToe
from agents.minimax_agent import MinimaxAgent
from agents.qlearning_agent import QLearningAgent

class TrainingManager:
    """
    Gerencia o treinamento do agente Q-Learning contra
    oponente aleatório ou Minimax, salvando Q-table e histórico
    incremental em history/history.csv a cada episódio.
    """
    def __init__(
        self,
        agent_symbol: str,
        opponent_type: str,
        num_episodes: int,
        log_interval: int = 100  # Intervalo para imprimir o status no console
    ):
        self.agent = QLearningAgent()
        self.agent_symbol    = agent_symbol        # 'X' ou 'O'
        self.opponent_type   = opponent_type.lower() # 'random' ou 'minimax'
        self.num_episodes    = num_episodes
        self.opponent_symbol = 'O' if agent_symbol == 'X' else 'X'
        self.log_interval    = log_interval

        # Prepara pasta e arquivo único de histórico
        os.makedirs("history", exist_ok=True)
        self.history_file = os.path.join("history", "history.csv")
        if not os.path.isfile(self.history_file):
            with open(self.history_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["episode", "wins", "draws", "losses", "epsilon"])

        # Se for vs Minimax, cria o agente adversário
        if self.opponent_type == 'minimax':
            self.minimax = MinimaxAgent(
                ai_player=self.opponent_symbol,
                human_player=self.agent_symbol
            )

    def train(self):
        """Escolhe o modo de treino conforme opponent_type."""
        if self.opponent_type == 'random':
            return self._train_vs_random()
        else:
            return self._train_vs_minimax()

    def _train_vs_random(self):
        stats = {'wins': 0, 'draws': 0, 'losses': 0}

        for ep in tqdm(range(1, self.num_episodes + 1),
                       desc="Treinando vs Random", unit="ep"):
            game = TicTacToe()
            state = game.get_state()
            done = False

            while not done:
                # Jogada do agente
                move = self.agent.choose_action(state, game.get_available_moves())
                game.make_move(move, self.agent_symbol)
                next_state = game.get_state()
                winner = game.check_winner()

                if winner is not None:
                    done = True
                    if winner == self.agent_symbol:
                        stats['wins'] += 1
                        r = 1.0
                    elif winner == 'Draw':
                        stats['draws'] += 1
                        r = 0.5
                    else:
                        stats['losses'] += 1
                        r = -1.0
                    self.agent.update_q(state, move, r, next_state, [])
                else:
                    # Jogada aleatória do oponente
                    opp = random.choice(game.get_available_moves())
                    game.make_move(opp, self.opponent_symbol)
                    ns2 = game.get_state()
                    self.agent.update_q(state, move, 0.0, ns2,
                                        game.get_available_moves())
                    state = ns2

            # Decaimento de epsilon
            self.agent.epsilon = max(self.agent.min_epsilon,
                                     self.agent.epsilon * self.agent.epsilon_decay)

            # Salva histórico e Q-table ao final de cada episódio
            self._append_history_entry(ep, stats['wins'], stats['draws'], stats['losses'], self.agent.epsilon)
            self.agent.save_q_table()

            # Log periódico no console
            if ep % self.log_interval == 0 or ep == self.num_episodes:
                tqdm.write(
                    f"{ep}/{self.num_episodes}: "
                    f"{stats['wins']} vitórias, {stats['draws']} empates, {stats['losses']} derrotas, ε={self.agent.epsilon:.4f}"
                )

        return stats, self.agent.epsilon

    def _train_vs_minimax(self):
        stats = {'wins': 0, 'draws': 0, 'losses': 0}

        for ep in tqdm(range(1, self.num_episodes + 1),
                       desc="Treinando vs Minimax", unit="ep"):
            game = TicTacToe()
            state = game.get_state()

            while True:
                # Jogada do agente
                move = self.agent.choose_action(state, game.get_available_moves())
                if move not in game.get_available_moves():
                    raise RuntimeError(f"Movimento inválido: {move}")
                game.make_move(move, self.agent_symbol)

                # Verifica término após agente
                w = game.check_winner()
                if w is not None:
                    if w == self.agent_symbol:
                        # Anomalia: o agente não deveria vencer o Minimax
                        stats['wins'] += 1
                        r = 1.0 # Recompensa alta por um evento raro
                        tqdm.write(f"[ANOMALIA] Minimax perdeu no episódio {ep}\n{game}")
                    elif w == 'Draw':
                        stats['draws'] += 1
                        r = 0.5
                    else: # Unreachable code if Minimax plays optimally
                        stats['losses'] += 1
                        r = -1.0
                    self.agent.update_q(state, move, r, game.get_state(), [])
                    break

                # Jogada do Minimax
                opp_move = self.minimax.find_best_move(game)
                if opp_move not in game.get_available_moves():
                    raise RuntimeError(f"Minimax jogou inválido: {opp_move}")
                game.make_move(opp_move, self.opponent_symbol)
                
                next_state_after_opp = game.get_state()
                winner_after_opp = game.check_winner()

                if winner_after_opp is not None:
                    # Agente perdeu ou empatou
                    if winner_after_opp == 'Draw':
                        stats['draws'] += 1
                        r = 0.5
                    else: # Agente perdeu
                        stats['losses'] += 1
                        r = -1.0
                    self.agent.update_q(state, move, r, next_state_after_opp, [])
                    break
                else:
                    # Jogo continua, estado intermediário
                    r = 0.0 # Recompensa neutra por sobreviver a um turno
                    self.agent.update_q(state, move, r, next_state_after_opp, game.get_available_moves())
                
                state = next_state_after_opp

            # Decaimento de epsilon
            self.agent.epsilon = max(self.agent.min_epsilon,
                                     self.agent.epsilon * self.agent.epsilon_decay)

            # Salva histórico e Q-table ao final de cada episódio
            self._append_history_entry(ep, stats['wins'], stats['draws'], stats['losses'], self.agent.epsilon)
            self.agent.save_q_table()

            # Log periódico no console
            if ep % self.log_interval == 0 or ep == self.num_episodes:
                tqdm.write(
                    f"{ep}/{self.num_episodes}: "
                    f"{stats['wins']} vitórias, {stats['draws']} empates, {stats['losses']} derrotas, ε={self.agent.epsilon:.4f}"
                )

        return stats, self.agent.epsilon

    def _append_history_entry(self, episode, wins, draws, losses, epsilon):
        """
        Acrescenta uma única linha com os resultados do episódio em history/history.csv.
        """
        with open(self.history_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                episode,
                wins,
                draws,
                losses,
                f"{epsilon:.6f}"
            ])