from tqdm import tqdm
from game.tic_tac_toe import TicTacToe
from agents.minimax_agent import MinimaxAgent
from agents.qlearning_agent import QLearningAgent


class TrainingManager:
    """
    Gerencia o treinamento do agente Q-Learning contra oponente aleatório ou Minimax.
    Inclui validação de movimentos e detecção de anomalias.
    """
    def __init__(self, agent_symbol: str, opponent_type: str, num_episodes: int):
        self.agent = QLearningAgent()
        self.agent_symbol = agent_symbol
        self.opponent_type = opponent_type
        self.num_episodes = num_episodes
        self.opponent_symbol = 'O' if agent_symbol == 'X' else 'X'

        if opponent_type == 'minimax':
            self.minimax = MinimaxAgent(
                ai_player=self.opponent_symbol,
                human_player=self.agent_symbol
            )

    def train(self):
        """
        Dispara o treinamento conforme o tipo de oponente escolhido.
        Retorna estatísticas de treino e epsilon final.
        """
        if self.opponent_type == 'random':
            from agents.qlearning_agent import train_q_learning
            return train_q_learning(
                self.agent,
                num_episodes=self.num_episodes,
                agent_symbol=self.agent_symbol
            )
        else:
            return self._train_vs_minimax()

    def _train_vs_minimax(self):
        stats = {'wins': 0, 'draws': 0, 'losses': 0}
        interval = max(1, self.num_episodes // 20)

        for episode in tqdm(
            range(1, self.num_episodes + 1),
            desc="Treinando",
            unit="ep"
        ):
            game = TicTacToe()
            state = game.get_state()

            while True:
                # Ação do agente Q-Learning
                available = game.get_available_moves()
                action = self.agent.choose_action(state, available)
                if action not in available:
                    raise RuntimeError(f"Movimento inválido pelo agente: {action}")
                game.make_move(action, self.agent_symbol)

                # Verifica término após jogada do agente
                winner = game.check_winner()
                if winner is not None:
                    # Detecção de anomalia: Minimax não pode perder
                    if winner == self.agent_symbol:
                        tqdm.write(
                            f"[Anomaly] Minimax perdeu no episódio {episode}. Tabuleiro:\n{game}"
                        )
                        break
                    # Empate ou vitória do Minimax
                    reward = self._get_reward(winner)
                    stats[self._get_stats_key(winner)] += 1
                    self.agent.update_q(state, action, reward, game.get_state(), [])
                    break

                # Ação do Minimax
                opp_move = self.minimax.find_best_move(game)
                available2 = game.get_available_moves()
                if opp_move not in available2:
                    raise RuntimeError(f"Movimento inválido pelo Minimax: {opp_move}")
                game.make_move(opp_move, self.opponent_symbol)

                # Verifica término após jogada do Minimax
                winner2 = game.check_winner()
                if winner2 is not None:
                    reward = self._get_reward(winner2)
                    stats[self._get_stats_key(winner2)] += 1
                    self.agent.update_q(state, action, reward, game.get_state(), [])
                    break

                # Estado intermediário: atualiza Q com recompensa zero
                next_state = game.get_state()
                next_moves = game.get_available_moves()
                self.agent.update_q(state, action, 0.0, next_state, next_moves)
                state = next_state

            # Decaimento de epsilon
            self.agent.epsilon = max(
                self.agent.min_epsilon,
                self.agent.epsilon * self.agent.epsilon_decay
            )

            # Feedback de progresso
            if episode % interval == 0 or episode == self.num_episodes:
                tqdm.write(
                    f"Progresso {episode}/{self.num_episodes}: "
                    f"{stats['wins']} vitórias, {stats['draws']} empates, {stats['losses']} derrotas. "
                    f"Epsilon: {self.agent.epsilon:.4f}"
                )

        self.agent.save_q_table()
        return stats, self.agent.epsilon

    def _get_reward(self, winner: str) -> float:
        if winner == 'Draw':
            return 0.5
        elif winner == self.agent_symbol:
            return 1.0
        else:
            return -1.0

    def _get_stats_key(self, winner: str) -> str:
        if winner == 'Draw':
            return 'draws'
        elif winner == self.agent_symbol:
            return 'wins'
        else:
            return 'losses'
