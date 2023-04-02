from random_agent import RandomAgent
from player import Player
from railroad import Railroad
from utility import Utility
from board import Board
from dice import Dice
from utilities import *
import copy
from strategy import Strategy
from property import Property

class Agent(RandomAgent):
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

    def buy_or_not(self, item, buy) -> int:
        if buy:
            return self.buy(item)
        return -1

    def action(self, board: Board, dice: Dice, buy: bool):
        location = self.move(dice.get_places())
        item = board.get_item_at_location(location)
        if location == 30:
            self.go_to_jail()
        elif isinstance(item, Property) or isinstance(item, Railroad) or isinstance(item, Utility):
            if item.get_owner() is None:
                cost = self.buy_or_not(item, buy)
            elif item.get_owner() != self and not item.is_mortgaged:
                if isinstance(item, Utility):
                    self.pay_rent(item.get_rent(dice.get_places()), item.get_owner(), item)
                else:
                    self.pay_rent(item.get_rent(), item.get_owner(), item)
        elif isinstance(item, int):
            self.pay_rent(item)

    def turn(self, other_player: Player, board: Board, dice: Dice):
        # self.display()
        self.strategy = Strategy(400, 2, 3, 5)
        self.turns += 1
        bestScore = float('-inf')
        best_stay_in_jail = True
        best_buy = None
        move = 0
        best_prop = None
        best_item = None
        if self.is_in_jail():
            for stay_in_jail in [True, False]:
                score = self.strategy.get_jail_heuristic(other_player, 1, board, stay_in_jail)
                if score >= bestScore:
                    bestScore = score
                    best_stay_in_jail = stay_in_jail
            self.jail_decide(dice, best_stay_in_jail)
        bestScore = float('-inf')
        first_copy = copy.deepcopy(self)
        if not self.is_in_jail():
            dice.roll(self)
            for buy in [True, False]:
                first_copy.action(board, dice, buy)
                for color in self.get_buildable_color_sets():
                    for prop in self.get_buildable_properties_on_color_set(color):
                        player_copy = copy.deepcopy(first_copy)
                        cost = prop.build_house()
                        player_copy.lose_money(cost)
                        player_copy.net_worth += cost / 2.0
                        score = player_copy.strategy.heuristic(other_player)
                        if bestScore <= score:
                            bestScore = score
                            move = 0
                            best_prop = prop # copies new prop!!!!
                            best_buy = buy
                for color in self.get_buildable_color_sets():
                    for prop in self.get_destroyable_properties_on_color_set(color):
                        player_copy = copy.deepcopy(first_copy)
                        cash = prop.destroy_house()
                        player_copy.gain_money(cash)
                        self.net_worth -= cash * 2
                        if bestScore <= score:
                            bestScore = score
                            move = 1
                            best_prop = prop
                            best_buy = buy
                for prop in self.get_buildable_properties():
                    if prop.get_number_of_houses() == 4 and Player.get_available_hotels() > 0:
                        player_copy = copy.deepcopy(first_copy)
                        cost = prop.upgrade_houses_to_hotel()
                        player_copy.lose_money(cost)
                        self.net_worth += 2 * cost
                        if bestScore <= score:
                            bestScore = score
                            move = 2
                            best_prop = prop
                            best_buy = buy
                for prop in self.get_downgradable_properties():
                    if Property.get_available_houses() > 3:
                        player_copy = copy.deepcopy(first_copy)
                        cost = prop.downgrade_hotel_to_houses()
                        player_copy.lose_money(cost)
                        self.net_worth += 8 * cost
                        if bestScore <= score:
                            bestScore = score
                            move = 3
                            best_prop = prop
                            best_buy = buy
                for props in self.properties.values():
                    for prop in props:
                        if not prop.is_mortgaged and prop.number_of_houses == 0 and prop.number_of_hotels == 0:
                            player_copy = copy.deepcopy(first_copy)
                            player_copy.gain_money(prop.mortgage())
                            if bestScore <= score:
                                bestScore = score
                                move = 4
                                best_item = prop
                                best_buy = buy
                for railroad in self.railroads:
                    if not railroad.is_mortgaged:
                        player_copy = copy.deepcopy(first_copy)
                        player_copy.gain_money(railroad.mortgage())
                        if bestScore <= score:
                            bestScore = score
                            move = 4
                            best_item = railroad
                            best_buy = buy
                for util in self.utilities:
                    if not util.is_mortgaged:
                        player_copy = copy.deepcopy(first_copy)
                        player_copy.gain_money(util.mortgage())
                        if bestScore <= score:
                            bestScore = score
                            move = 4
                            best_item = util
                            best_buy = buy
                for props in self.properties.values():
                    for prop in props:
                        if prop.is_mortgaged:
                            player_copy = copy.deepcopy(first_copy)
                            player_copy.lose_money(prop.unmortgage())
                            if bestScore <= score:
                                bestScore = score
                                move = 5
                                best_item = prop
                                best_buy = buy
                for railroad in self.railroads:
                    if railroad.is_mortgaged:
                        player_copy = copy.deepcopy(first_copy)
                        player_copy.lose_money(railroad.unmortgage())
                        if bestScore <= score:
                            bestScore = score
                            move = 5
                            best_item = railroad
                            best_buy = buy
                for util in self.utilities:
                    if util.is_mortgaged:
                        player_copy = copy.deepcopy(first_copy)
                        player_copy.lose_money(util.unmortgage())
                        if bestScore <= score:
                            bestScore = score
                            move = 5
                            best_item = util
                            best_buy = buy
        if best_item == None or best_prop == None or best_buy == None:
            return
        self.action(board, dice, best_buy)
        match move:
            case 0:
                cost = best_prop.build_house()
                self.lose_money(cost)
                self.net_worth += cost / 2.0
            case 1:
                cash = best_prop.destroy_house()
                self.gain_money(cash)
                self.net_worth -= cash * 2
            case 2:
                cost = best_prop.upgrade_houses_to_hotel()
                self.lose_money(cost)
                self.net_worth += 2 * cost
            case 3:
                cost = best_prop.downgrade_hotel_to_houses()
                self.lose_money(cost)
                self.net_worth += 8 * cost
            case 4:
                self.gain_money(best_item.mortgage())
            case 5:
                self.lose_money(best_item.mortgage())

if __name__ == '__main__':
    board = Board()
    player1 = FirstAgent('player1')
    player2 = FirstAgent('player2')
    board.map[13].owner = player2
    board.map[19].owner = player2
    board.map[16].owner = player1
    player2.location = 10
    score = player2.get_jail_heuristic(player1, 1, board, False)