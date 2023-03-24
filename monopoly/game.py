from random import shuffle
from player import Player
from board import Board
from dices import Dices

class Game:
    def __init__(self, players_num: int=2): # the implementation considers only 2 players
        self.players = [Player() for _ in range(players_num)]

    def play(self):
        suffle(self.players)
        limit = 10000
        dices = Dices()
        i = 0
        for _ in range(limit):
            player = self.players[i]
            dices.roll()
            player.move(dices.get_places)
            while dices.is_double():
                if dices.get_double_counter > 2:
                    player.go_to_jail()
                else:
                    dices.roll()
                    player.move(dices.get_places)
            i = 1 - i