import game
from random_agent import RandomAgent
from agent import Agent
import player
from tqdm import tqdm

def play_test_game(player1: player.Player, player2: player.Player):
    test_game = game.Game(player1, player2)
    test_game.play()

def evaluate(games_num, player1_class, player2_class):
    player1_wins = 0
    player2_wins = 0
    total_turns = 0.0
    i = 0
    while i < games_num:
        player1 = player1_class('player1')
        player2 = player2_class('player2')
        test_game = game.Game(player1, player2)
        test_game.play()
        if test_game.winner == player1:
            player1_wins += 1
        elif test_game.winner == player2:
            player2_wins += 1
        #else:
         #   continue
        total_turns += test_game.turns
        i += 1
    print(f'{player1.name} wins {player1_wins} times.')
    print(f'{player2.name} wins {player2_wins} times.')
    print(f'{player1.name} wins {player1_wins * 100.0 / games_num}% of the time.')
    print(f'{player2.name} wins {player2_wins * 100.0 / games_num}% of the time.')
    print(f'total number of games played: {games_num}')
    print(f'average number of turns: {total_turns / games_num}')

if __name__ == '__main__':
    # player_bot = random_agent.RandomAgent('player_bot')
    # player_human = player.Player('player_human')
    # player_human = random_agent.RandomAgent('player_human')
    # play_test_game(player_bot, player_human)
    # ================== AGENT EVALUATION ===============================
    # =========== random agent vs random agent ==========================
    #evaluate(100, RandomAgent, RandomAgent)
    # =========== random agent vs agent ============================
    #evaluate(5, RandomAgent, Agent)
    # =========== agent vs agent ============================
    evaluate(1, Agent, Agent)