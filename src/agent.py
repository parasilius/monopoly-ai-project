from player import Player
from property import Property
from board import Board
from railroad import  Railroad
from utility import Utility
from dice import Dice
import random
from utilities import *
import copy

class Agent(Player):
    def buy_or_not(self, item, buy: bool) -> int:
        if buy:
            return self.buy(item)
        return -1

    def get_buildable_color_sets(self): # do we need get_buildable_properties instead?!
        color_sets = ['brown', 'light blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark blue']
        for color in color_sets:
            if self.check_has_all_in_color_set(color):
                yield color
    
    def get_buildable_properties(self):
        for color in self.get_buildable_color_sets():
            for prop in self.get_destroyable_properties_on_color_set(color):
                yield prop
    
    def build_or_not_in_color_set(self, color: str, build: bool):
        # print_with_color(f'speaking of {color} set...', self)
        if build:
            for prop in self.get_buildable_properties_on_color_set(color):
                cost = prop.build_house()
                self.lose_money(cost)
                self.net_worth += cost / 2.0
    
    def build_or_not(self):
        color_sets = ['brown', 'light blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark blue']
        available_color_sets = []
        for color in color_sets:
            if self.check_has_all_in_color_set(color):
                available_color_sets.append(color)
        for color in available_color_sets:
            # print_with_color(f'speaking of {color} set...', self)
            if bool(random.getrandbits(1)):
                for prop in self.get_buildable_properties_on_color_set(color):
                    cost = prop.build_house()
                    self.lose_money(cost)
                    self.net_worth += cost / 2.0
            for prop in self.properties[color]:
                if prop.get_number_of_houses() == 4 and Player.get_available_hotels() > 0:
                    if bool(random.getrandbits(1)):
                        cost = prop.upgrade_houses_to_hotel()
                        self.lose_money(cost)
                        self.net_worth += 2 * cost
                if prop.get_number_of_hotels() == 1 and Player.get_available_houses() > 3:
                    if bool(random.getrandbits(1)):
                        cost = prop.downgrade_hotel_to_houses()
                        self.lose_money(cost)
                        self.net_worth += 8 * cost

    def get_properties_with_hotel(self):
        for prop in self.get_buildable_properties():
            if prop.number_of_hotels > 0:
                yield prop

    def upgrade_hotel_or_not(self): #hotels
        for prop in self.properties[color]:
            if prop.get_number_of_houses() == 4 and Property.get_available_hotels() > 0:
                if bool(random.getrandbits(1)):
                    cost = prop.upgrade_houses_to_hotel()
                    self.lose_money(cost)
                    self.net_worth += 2 * cost
    
    def downgrade_hotel_or_not(self):
        for prop in self.get_properties_with_hotel():
            if prop.get_number_of_hotels() == 1 and Property.get_available_houses() > 3:
                if bool(random.getrandbits(1)):
                    cost = prop.downgrade_hotel_to_houses()
                    self.lose_money(cost)
                    self.net_worth += 8 * cost
    
    def action(self, board: Board, dice: Dice, buy: bool):
        location = self.move(dice.get_places())
        item = board.get_item_at_location(location)
        if location == 30:
            self.go_to_jail()
        elif isinstance(item, Property):
            if item.get_owner() is None:
                cost = self.buy_or_not(item, buy)
                if cost != -1:
                    # pass
                    print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner().name != self.name and not item.is_mortgaged:
                self.pay_rent(item.get_rent(), item.get_owner(), item)
        elif isinstance(item, Railroad):
            if item.get_owner() is None:
                cost = self.buy_or_not(item, buy)
                if cost != -1:
                    # pass
                    print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner().name != self.name:
                self.pay_rent(2 ** (item.get_owner().get_number_of_railroads() - 1) * 25, item.get_owner(), item)
        elif isinstance(item, Utility):
            if item.get_owner() is None:
                cost = self.buy_or_not(item, buy)
                if cost != -1:
                    # pass
                    print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner().name != self.name:
                if item.get_owner().get_number_of_utilities() == 1:
                    self.pay_rent(dice.get_places() * 4, item.get_owner(), item)
                else: # owner's number of utilities is 2
                    self.pay_rent(dice.get_places() * 10, item.get_owner(), item)
        elif isinstance(item, int):
            self.pay_rent(item)
    
    def mortgage_or_not(self):
        pass

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
    
    def evaluate_state(self, other_player: Player, board: Board, stay_in_jail: bool) -> float:
        if self.is_bankrupt:
            return float('-inf')
        if other_player.is_bankrupt:
            return float('+inf')
        score = 0
        if stay_in_jail:
            for props in other_player.properties.values():
                for prop in props:
                    score -= prop.lprobability * prop.get_rent()
        else: # if was in jail, but decided to go out
            for props in other_player.properties.values():
                for prop in props:
                    score -= prop.sprobability * prop.get_rent()
        return score

    def get_heuristic(self, other_player: Player, isMaximizing: bool, depth: int, board: Board, dice: Dice, stay_in_jail: bool) -> int:
        if depth == 0:
            return self.evaluate_state(other_player, board, stay_in_jail)
        elif depth == 3:
            bestScore = 0
            for i in range(1, 7):
                for j in range(1, 7):
                    self.location += i + j
                    bestScore += (1 / 36.0) * self.get_heuristic(other_player, isMaximizing, depth - 1, board, dice, stay_in_jail)
        elif isMaximizing:
            bestScore = float('-inf')
            for stay_in_jail in [True, False]:
                return max(bestScore, self.get_heuristic(other_player, isMaximizing, depth - 1, board, dice, stay_in_jail))
        else:
            bestScore = float('+inf')
            for stay_in_jail in [True, False]:
                return min(bestScore, self.get_heuristic(other_player, 'final', depth - 1, board, dice, stay_in_jail))
        return bestScore
    
    def turn(self, other_player: Player, board: Board, dice: Dice):
        # self.display()
        self.turns += 1
        bestScore = float('-inf')
        best_stay_in_jail = True
        player_copy = copy.deepcopy(self)
        if self.is_in_jail():
            for stay_in_jail in [True, False]:
                score = player_copy.get_heuristic(other_player, True, 2, board, dice, stay_in_jail)
                if score > bestScore:
                    bestScore = score
                    best_stay_in_jail = stay_in_jail
            self.jail_decide(dice, best_stay_in_jail)
        if not self.is_in_jail():
            dice.roll(self)
            self.action(board, dice, bool(random.getrandbits(1)))
        match (self.turns - 1) % 4:
            case 0:
                self.build_or_not()
            case 1:
                self.destroy_or_not()
            case 2:
                self.mortgage_or_not()
            case 3:
                self.unmortgage_or_not()