import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import sys

# Constantes
HISTORY_FILE = os.path.join('history', 'history.csv')
UPDATE_INTERVAL_MS = 280  # Atualiza o gráfico

# Configuração inicial do Gráfico
fig, ax1 = plt.subplots(figsize=(12, 7))
ax2 = ax1.twinx()  # Cria um segundo eixo Y para o Epsilon

# Adiciona um título inicial
fig.suptitle('Aguardando dados do treinamento...', fontsize=16)

def animate(i):
    """
    Função que lê os dados e atualiza o gráfico.
    É chamada periodicamente pela FuncAnimation.
    """
    if not os.path.exists(HISTORY_FILE):
        return

    try:
        data = pd.read_csv(HISTORY_FILE)
        if data.empty:
            return
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return
    
    # Extrai as colunas
    episodes = data['episode']
    wins = data['wins']
    draws = data['draws']
    losses = data['losses']
    epsilon = data['epsilon']

    # Calcula a taxa de vitória (Win Rate)
    total_games = wins + draws + losses
    win_rate = (wins / total_games.replace(0, 1)) * 100

    # Limpa os eixos para redesenhar
    ax1.cla()
    ax2.cla()

    # --- Eixo 1: Taxa de Vitória e Contagens ---
    ax1.plot(episodes, win_rate, label='Taxa de Vitória (%)', color='green', linewidth=2)
    ax1.plot(episodes, draws, label='Empates', color='orange', linestyle='--')
    ax1.plot(episodes, losses, label='Derrotas', color='red', linestyle='--')
    
    ax1.set_xlabel('Episódios', fontsize=12)
    ax1.set_ylabel('Contagem / Taxa de Vitória (%)', color='black', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(axis='y', linestyle=':', linewidth=0.7)

    # --- Eixo 2: Epsilon ---
    ax2.plot(episodes, epsilon, label='Epsilon (ε)', color='purple', linestyle=':')
    #ax2.set_ylabel('Epsilon (ε)', color='purple', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='purple')
    ax2.set_ylim(-0.05, 1.05) # Ajustado o limite superior para 1.05

    # --- Título e Legenda (CORRIGIDO) ---
    # Pega o último valor de cada série para exibir no título
    last_episode = episodes.iloc[-1]
    last_wins = wins.iloc[-1]
    last_draws = draws.iloc[-1]
    last_losses = losses.iloc[-1]
    last_epsilon = epsilon.iloc[-1]

    # Usa os valores únicos no título
    fig.suptitle(
        f"Episódio: {last_episode} | "
        f"{last_wins} {((last_wins/last_episode)*100):.2f}% vitórias,"
        f"{last_draws} {((last_draws/last_episode)*100):.2f}% empates,"
        f"{last_losses} {((last_losses/last_episode)*100):.2f}% derrotas | "
        f"ε={last_epsilon:.4f}",
        fontsize=14
    )
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# Inicia a animação
ani = FuncAnimation(fig, animate, interval=UPDATE_INTERVAL_MS, cache_frame_data=False)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

print("Janela de plotagem fechada.")