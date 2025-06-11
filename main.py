import argparse
from training_manager import TrainingManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--train', action='store_true', help='Executa treinamento de Q-Learning'
    )
    parser.add_argument(
        '--opponent', choices=['random', 'minimax'], default='random',
        help='Tipo de oponente durante o treino'
    )
    parser.add_argument(
        '--episodes', type=int, default=5000,
        help='Número de episódios de treino'
    )
    parser.add_argument(
        '--symbol', choices=['X', 'O'], default='X',
        help='Símbolo do agente Q-Learning'
    )
    args = parser.parse_args()

    if args.train:
        manager = TrainingManager(
            agent_symbol=args.symbol,
            opponent_type=args.opponent,
            num_episodes=args.episodes
        )
        stats, eps = manager.train()
        print(
            f"Treino concluído: {stats['wins']} vitórias, {stats['draws']} empates, {stats['losses']} derrotas. "
            f"Epsilon final: {eps:.4f}"
        )
    else:
        print(
            "Modo de jogo ainda não implementado. Use --train para treinar."
        )


if __name__ == '__main__':
    main()
