from random import shuffle
from player import Player
from board import Board
from dice import Dice
from property import Property
from railroad import Railroad
from utility import Utility

class Game:
    def __init__(self, player1: Player, player2: Player): # the implementation considers only 2 players
        self.players = [player1, player2]
        self.winner = None
        self.turns = 0
    
    def play(self):
        shuffle(self.players)
        limit = 10000
        dice = Dice()
        i = 0
        board = Board()
        for _ in range(limit):
            player = self.players[i]
            if self.players[0].is_bankrupt():
                self.winner = self.players[1]
                print(f'player {self.winner.player_name} wins.')
                print(f'total turns played: {self.turns}')
                break
            if self.players[1].is_bankrupt():
                self.winner = self.players[0]
                print(f'player {self.winner.player_name} wins.')
                print(f'total turns played: {self.turns}')
                break
            player.turn(board, dice)
            double_counter = 0
            while dice.is_double():
                double_counter += 1
                if double_counter > 2:
                    player.go_to_jail()
                    double_counter = 0
                    break
                else:
                    player.turn(board, dice)
            i = 1 - i
        self.turns = self.players[0].turns + self.players[1].turns

if __name__ == '__main__':
    game = Game()
    game.play()