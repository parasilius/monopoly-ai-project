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

class Agent(RandomAgent):
    def action(self, board: Board, dice: Dice):
        location = self.move(dice.get_places())
        item = board.get_item_at_location(location)
        if location == 30:
            self.go_to_jail()
        elif isinstance(item, Property):
            if item.get_owner() is None:
                cost = self.buy_or_not(item)
                if cost != -1:
                    pass
                    # print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner().name != self.name and not item.is_mortgaged:
                self.pay_rent(item.get_rent(), item.get_owner(), item)
        elif isinstance(item, Railroad):
            if item.get_owner() is None:
                cost = self.buy_or_not(item)
                if cost != -1:
                    pass
                    # print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner().name != self.name:
                self.pay_rent(2 ** (item.get_owner().get_number_of_railroads() - 1) * 25, item.get_owner(), item)
        elif isinstance(item, Utility):
            if item.get_owner() is None:
                cost = self.buy_or_not(item)
                if cost != -1:
                    pass
                    # print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner().name != self.name:
                if item.get_owner().get_number_of_utilities() == 1:
                    self.pay_rent(dice.get_places() * 4, item.get_owner(), item)
                else: # owner's number of utilities is 2
                    self.pay_rent(dice.get_places() * 10, item.get_owner(), item)
        elif isinstance(item, int):
            self.pay_rent(item)
    
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
    
    def evaluate_jail_stay(self, other_player: Player, board: Board, dice: Dice, stay_in_jail: bool) -> float:
        if self.is_bankrupt():
            return float('-inf')
        if other_player.is_bankrupt():
            return float('+inf')
        if stay_in_jail:
            return 0
        elif board.map[self.location] != None and not isinstance(board.map[self.location], int):
            if board.map[self.location].owner != None and board.map[self.location].owner.name == other_player.name and not board.map[self.location].is_mortgaged:
                if isinstance(board.map[self.location], Utility):
                    return -1 * board.map[self.location].get_rent(dice)
                else:
                    return -1 * board.map[self.location].get_rent()
            elif board.map[self.location].owner == None:
                self.buy(board.map[self.location]) # buying is better than not buying in the first turns
                if isinstance(board.map[self.location], Utility):
                    return board.map[self.location].lprobability * 28 # 28 isn't a good choice, but sufficient
                else:
                    return board.map[self.location].lprobability * board.map[self.location].get_rent() # doesn't change net worth
        return 0

    def get_jail_heuristic(self, other_player: Player, depth: int, board: Board, dice: Dice, stay_in_jail: bool) -> float:
        if stay_in_jail or depth == 0 or self.is_bankrupt() or other_player.is_bankrupt():
            return self.evaluate_jail_stay(other_player, board, dice, stay_in_jail)
        else:
            bestScore = 0
            player_copy = copy.deepcopy(self)
            for i in range(1, 7):
                for j in range(1, 7):
                    player_copy = copy.deepcopy(self)
                    player_copy.lose_money(50)
                    player_copy.location += i + j
                    bestScore += (1 / 36.0) * player_copy.get_jail_heuristic(other_player, depth - 1, board, dice, False)
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
                score = self.get_jail_heuristic(other_player, 1, board, dice, stay_in_jail)
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