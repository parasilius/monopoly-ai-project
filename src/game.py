from random import shuffle
from player import Player
from board import Board
from dice import Dice

class Game:
    def __init__(self, player1: Player, player2: Player): # the implementation considers only 2 players
        self.players = [player1, player2]
        self.winner = None
        self.turns = 0
        self.board = Board()
        self.dice = Dice()
    
    def play(self):
        shuffle(self.players)
        limit = 10000
        i = 0
        for _ in range(limit):
            player = self.players[i]
            other_player = self.players[1 - i]
            if player.is_bankrupt():
                self.winner = other_player
                print(f'{other_player.name} wins.')
                break
            if other_player.is_bankrupt():
                self.winner = player
                print(f'{player.name} wins.')
                break
            player.turn(other_player, self.board, self.dice)
            double_counter = 0
            while self.dice.is_double():
                double_counter += 1
                if double_counter > 2:
                    player.go_to_jail()
                    double_counter = 0
                    break
                else:
                    player.turn(other_player, self.board, self.dice)
            i = 1 - i
        self.turns = self.players[0].turns + self.players[1].turns
        print(f'total turns played: {self.turns}')

if __name__ == '__main__':
    player1 = Player('player1')
    player2 = Player('player2')
    game = Game(player1, player2)
    game.play()