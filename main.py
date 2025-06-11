import argparse
from tqdm import tqdm
from game.tic_tac_toe import TicTacToe
from agents.minimax_agent import MinimaxAgent
from agents.qlearning_agent import QLearningAgent, train_q_learning


def train_random_opponent(agent: QLearningAgent, num_episodes: int, agent_symbol: str):
    """
    Treina o agente contra oponente aleatório.
    """
    return train_q_learning(agent, num_episodes=num_episodes, agent_symbol=agent_symbol)


def train_vs_minimax(
    agent: QLearningAgent,
    minimax: MinimaxAgent,
    num_episodes: int,
    agent_symbol: str
):
    """
    Treina o agente contra um MinimaxAgent, com detecção de terminação após cada jogada.
    Exibe progresso via tqdm.
    """
    opponent_symbol = 'O' if agent_symbol == 'X' else 'X'
    stats = {'wins': 0, 'draws': 0, 'losses': 0}
    interval = max(1, num_episodes // 10)

    for episode in tqdm(range(1, num_episodes + 1), desc="Treinando vs Minimax", unit="ep"):
        game = TicTacToe()
        state = game.get_state()
        done = False

        while not done:
            # Jogada do agente Q-Learning
            available = game.get_available_moves()
            action = agent.choose_action(state, available)
            game.make_move(action, agent_symbol)
            next_state = game.get_state()
            winner = game.check_winner()

            if winner is not None:
                # Termina partida após jogada do agente
                done = True
                if winner == agent_symbol:
                    reward = 1.0
                    stats['wins'] += 1
                elif winner == 'Draw':
                    reward = 0.5
                    stats['draws'] += 1
                else:
                    reward = -1.0
                    stats['losses'] += 1
                agent.update_q(state, action, reward, next_state, [])
                break

            # Jogada do Minimax
            opp_move = minimax.find_best_move(game)
            game.make_move(opp_move, opponent_symbol)
            next_state2 = game.get_state()
            winner2 = game.check_winner()

            if winner2 is not None:
                # Termina partida após jogada do Minimax
                done = True
                if winner2 == agent_symbol:
                    reward = 1.0
                    stats['wins'] += 1
                elif winner2 == 'Draw':
                    reward = 0.5
                    stats['draws'] += 1
                else:
                    reward = -1.0
                    stats['losses'] += 1
                agent.update_q(state, action, reward, next_state2, [])
                break

            # Atualização pós-movimento não-terminal
            reward = 0.0
            agent.update_q(state, action, reward, next_state2, game.get_available_moves())
            state = next_state2

        # Decaimento de epsilon
        agent.epsilon = max(agent.min_epsilon, agent.epsilon * agent.epsilon_decay)

        # Feedback de progresso a cada 10%
        if episode % interval == 0 or episode == num_episodes:
            tqdm.write(
                f"Progresso {episode}/{num_episodes}: "
                f"{stats['wins']} vitórias, {stats['draws']} empates, {stats['losses']} derrotas. "
                f"Epsilon: {agent.epsilon:.4f}"
            )

    agent.save_q_table()
    return stats, agent.epsilon


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true', help='Executa treinamento de Q-Learning')
    parser.add_argument('--opponent', choices=['random', 'minimax'], default='random',
                        help='Tipo de oponente durante o treino')
    parser.add_argument('--episodes', type=int, default=5000, help='Número de episódios de treino')
    parser.add_argument('--symbol', choices=['X', 'O'], default='X', help='Símbolo do agente Q-Learning')
    args = parser.parse_args()

    if args.train:
        agent = QLearningAgent()

        if args.opponent == 'random':
            stats, eps = train_random_opponent(agent, args.episodes, args.symbol)
        else:
            # Configura MinimaxAgent como oponente
            opponent_symbol = 'O' if args.symbol == 'X' else 'X'
            minimax = MinimaxAgent(ai_player=opponent_symbol, human_player=args.symbol)
            stats, eps = train_vs_minimax(agent, minimax, args.episodes, args.symbol)

        print(
            f"Treino concluído: {stats['wins']} vitórias, {stats['draws']} empates, "
            f"{stats['losses']} derrotas. Epsilon final: {eps:.4f}"
        )
    else:
        # Lógica de jogo interativo em Pygame (a implementar)
        print("Modo de jogo ainda não implementado. Use --train para treinar.")


if __name__ == '__main__':
    main()
