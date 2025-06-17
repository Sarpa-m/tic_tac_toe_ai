# Tic-Tac-Toe AI - Agentes Inteligentes para o Jogo da Velha

Este projeto apresenta uma implementação completa do Jogo da Velha, destacando a criação e o treinamento de agentes de Inteligência Artificial. A aplicação possui uma interface gráfica desenvolvida com Tkinter e permite que os usuários joguem contra diferentes tipos de IA ou observem as IAs jogando entre si.

O foco principal é a demonstração e comparação de duas abordagens clássicas de IA para jogos de tabuleiro:

1.  **Agente Minimax**: Uma IA determinística que utiliza o algoritmo Minimax para realizar buscas exaustivas no espaço de estados do jogo. O resultado é um agente que joga de forma "perfeita", sendo impossível vencê-lo (o melhor resultado possível para um oponente é o empate).

2.  **Agente Q-Learning**: Uma IA baseada em Aprendizado por Reforço. Este agente não possui conhecimento prévio das regras e aprende a jogar através de milhares de partidas de treinamento. Ele utiliza uma Tabela Q para associar o valor de cada ação a cada estado do jogo, refinando sua estratégia com base em recompensas e punições.

O projeto é dividido em um modo de **treinamento**, executado via linha de comando, e um modo de **jogo**, com interface gráfica.

## 🚀 Funcionalidades

  * **Lógica de Jogo Encapsulada**: As regras do Jogo da Velha são isoladas em sua própria classe, permitindo fácil manutenção e reutilização.
  * **Múltiplos Agentes**: Jogue como humano ou escolha entre agentes: Aleatório, Minimax (imbatível) ou Q-Learning (aprendiz).
  * **Treinamento Configurável**: Treine o agente Q-Learning contra um oponente aleatório ou o poderoso Minimax para refinar sua Tabela Q.
  * **Persistência de Conhecimento**: A Tabela Q do agente é salva em um arquivo `q_table.json`, permitindo que o aprendizado seja retomado a qualquer momento.
  * **Visualização do Treinamento**: Um script separado permite plotar gráficos em tempo real, mostrando a evolução da performance do agente (taxa de vitórias, empates, derrotas) e a variação do `epsilon` ao longo dos episódios.
  * **Interface Gráfica Intuitiva**: Uma UI simples construída com Tkinter para configurar e jogar as partidas.

## 🛠️ Estrutura do Projeto

O código é organizado de forma modular para separar as responsabilidades:

  - `game/`: Contém a lógica fundamental do jogo (`tic_tac_toe.py`).
  - `agents/`: Contém as implementações dos agentes de IA (`minimax_agent.py`, `qlearning_agent.py`).
  - `ui_tk/`: Contém todos os componentes da interface gráfica.
  - `history/`: Pasta onde o histórico de treinamento é salvo (`history.csv`).
  - `main.py`: Ponto de entrada que direciona para o modo de jogo ou treinamento.
  - `training_manager.py`: Orquestra as sessões de treinamento.
  - `plot_live.py`: Script para visualização do progresso do treinamento.

## ⚙️ Instalação e Execução

Para executar o projeto, você precisará do Python 3. É altamente recomendável usar um ambiente virtual.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/sarpa-m/tic_tac_toe_ai.git
    cd tic_tac_toe_ai
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Para Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências a partir do `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

## 🎮 Como Jogar

Para iniciar a interface gráfica e jogar, basta executar o `main.py` sem argumentos:

```bash
python main.py
```

Na tela do jogo, você pode:

  - Selecionar o tipo de jogador para 'X' e 'O' (Humano, Minimax, Q-Learning, Aleatório).
  - Definir o número de partidas a serem jogadas em sequência.
  - Ajustar a velocidade (atraso em milissegundos) entre as jogadas das IAs.

## 🧠 Treinando a IA

Para treinar o agente Q-Learning, utilize a flag `--train` na linha de comando. Você pode configurar o oponente, o número de episódios e o símbolo do agente.

**Exemplo 1: Treinar por 10.000 episódios contra um oponente aleatório.**

```bash
python main.py --train --episodes 10000 --opponent random
```

**Exemplo 2: Treinamento avançado por 5.000 episódios contra o agente Minimax.**

```bash
python main.py --train --episodes 5000 --opponent minimax
```

### Visualização em Tempo Real

Enquanto o treinamento está em execução em um terminal, você pode abrir **um segundo terminal** (com o mesmo ambiente virtual ativado) e executar o `plot_live.py` para ver o progresso:

```bash
python plot_live.py
```

Isso abrirá uma janela do Matplotlib que se atualiza automaticamente, mostrando a taxa de vitórias, empates, derrotas e o decaimento do `epsilon`.

## 💡 Destaques do Código



### Lógica do Jogo: `check_winner()`

A verificação de vitória é feita de forma sistemática, checando todas as 8 combinações possíveis.

```python
# Em game/tic_tac_toe.py
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
```

### Agente Minimax: A Recursão

O núcleo do Minimax é uma função recursiva que alterna entre maximizar a pontuação da IA e minimizar a pontuação do oponente.

```python
# Em agents/minimax_agent.py
def minimax(self, board: TicTacToe, depth: int, is_maximizing: bool) -> int:
    """Função recursiva Minimax."""
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
```

### Agente Q-Learning: A Equação de Aprendizado

A atualização da Tabela Q é feita usando a equação de Bellman, que combina a recompensa imediata com a melhor recompensa futura esperada.

```python
# Em agents/qlearning_agent.py
def update_q(self, state: tuple, action: int, reward: float, next_state: tuple, next_moves: list):
    key = self._state_key(state)
    # ...
    old_q = self.q_table[key].get(str(action), 0.0)
    future_q = 0.0
    if next_moves:
        future_q = max(self.get_q(next_state, a) for a in next_moves)
    
    # Equação de Bellman
    new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
    self.q_table[key][str(action)] = new_q
```

### Gerenciador de Treinamento: O Loop

O `TrainingManager` orquestra os episódios de treinamento, alternando as jogadas e acionando o aprendizado do agente.

```python
# Em training_manager.py
def _train_vs_random(self):
    # ...
    for ep in tqdm(range(1, self.num_episodes + 1), ...):
        game = TicTacToe()
        state = game.get_state()
        done = False

        while not done:
            # Jogada do agente
            move = self.agent.choose_action(state, game.get_available_moves())
            game.make_move(move, self.agent_symbol)
            # ... verifica fim de jogo ...

            # Jogada aleatória do oponente
            opp = random.choice(game.get_available_moves())
            game.make_move(opp, self.opponent_symbol)
            
            # Agente aprende com o resultado da rodada
            ns2 = game.get_state()
            self.agent.update_q(state, move, 0.0, ns2, game.get_available_moves())
            state = ns2
```
