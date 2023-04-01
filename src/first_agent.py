from random_agent import RandomAgent
from player import Player
from property import Property
from board import Board
from railroad import  Railroad
from utility import Utility
from dice import Dice
import random
from utilities import *
import copy

class FirstAgent(RandomAgent):    
    def jail_decide(self, dice: Dice, stay_in_jail: bool):
        if not stay_in_jail:
            self.lose_money(50)
            self.get_out_of_jail()
        else:
            dice.roll(self)
            if dice.is_double():
                self.get_out_of_jail()
            elif self.jail_times_increment() > 2:
                self.lose_money(50)
                self.get_out_of_jail()
            else:
                return False
        return True
    
    def evaluate_jail_stay(self, other_player: Player, board: Board, stay_in_jail: bool) -> float:
        if self.is_bankrupt():
            return float('-inf')
        if stay_in_jail:
            return 0
        elif board.map[self.location] != None and not isinstance(board.map[self.location], int):
            if board.map[self.location].owner != None and board.map[self.location].owner.name == other_player.name and not board.map[self.location].is_mortgaged:
                if isinstance(board.map[self.location], Utility):
                    self.pay_rent(board.map[self.location].get_rent(2)) # no need for other arguments
                else:
                    self.pay_rent(board.map[self.location].get_rent()) # no need for other arguments
                if self.is_bankrupt():
                    return float('-inf')
                return -1
            elif board.map[self.location].owner == None:
                self.buy(board.map[self.location]) # buying is better than not buying in the first turns
                if self.is_bankrupt():
                    return float('-inf')
                if isinstance(board.map[self.location], Utility):
                    return 0
                return 1
        return 0

    def get_jail_heuristic(self, other_player: Player, depth: int, board: Board, stay_in_jail: bool) -> float:
        if stay_in_jail or depth == 0 or self.is_bankrupt() or other_player.is_bankrupt():
            return self.evaluate_jail_stay(other_player, board, stay_in_jail)
        else:
            bestScore = 0
            for i in range(1, 7):
                for j in range(1, 7):
                    player_copy = copy.deepcopy(self)
                    player_copy.lose_money(50)
                    player_copy.location += i + j
                    bestScore += (1 / 36.0) * player_copy.get_jail_heuristic(other_player, depth - 1, board, False)
                    player_copy.location -= i + j
            return bestScore
    
    def turn(self, other_player: Player, board: Board, dice: Dice):
        # self.display()
        self.turns += 1
        bestScore = float('-inf')
        best_stay_in_jail = True
        # player_copy = copy.deepcopy(self)
        if self.is_in_jail():
            for stay_in_jail in [True, False]:
                score = self.get_jail_heuristic(other_player, 1, board, stay_in_jail)
                if score >= bestScore:
                    bestScore = score
                    best_stay_in_jail = stay_in_jail
            self.jail_decide(dice, best_stay_in_jail)
        if not self.is_in_jail():
            dice.roll(self)
            self.action(board, dice)
        match (self.turns - 1) % 6:
            case 0:
                self.build_or_not()
            case 1:
                self.destroy_or_not()
            case 2:
                self.upgrade_houses_or_not()
            case 3:
                self.downgrade_hotel_or_not()
            case 4:
                self.mortgage_or_not()
            case 5:
                self.unmortgage_or_not()

if __name__ == '__main__':
    board = Board()
    player1 = FirstAgent('player1')
    player2 = FirstAgent('player2')
    board.map[13].owner = player2
    board.map[19].owner = player2
    board.map[16].owner = player1
    player2.location = 10
    score = player2.get_jail_heuristic(player1, 1, board, False)