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
    def jail_decide(self, stay_in_jail: bool):
        if not stay_in_jail:
            self.lose_money(50)
            self.get_out_of_jail()

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
        self.display()
        self.strategy = Strategy(400, 2, 3, 5)
        self.turns += 1
        bestScore = float('-inf')
        best_stay_in_jail = True
        move = None
        if self.is_in_jail():
            for stay_in_jail in [True, False]:
                score = self.strategy.get_jail_heuristic(self, other_player, 1, board, stay_in_jail)
                if score >= bestScore:
                    bestScore = score
                    best_stay_in_jail = stay_in_jail
            self.jail_decide(best_stay_in_jail)
        dice.roll(self)
        if self.is_in_jail() and (dice.is_double() or self.jail_times_increment() > 2):
            self.lose_money(50)
            self.get_out_of_jail()
        if not self.is_in_jail():
            print('start')
            best_buy, move, best_location = self.strategy.decide(self, other_player, board, dice)
            print('done')
            if best_buy == None or best_location == None:
                return
            self.action(board, dice, best_buy)
        if move is not None:
            match move:
                case 0:
                    cost = board.map[best_location].build_house()
                    self.lose_money(cost)
                    self.net_worth += cost / 2.0
                case 1:
                    cash = board.map[best_location].destroy_house()
                    self.gain_money(cash)
                    self.net_worth -= cash * 2
                case 2:
                    cost = board.map[best_location].upgrade_houses_to_hotel()
                    self.lose_money(cost)
                    self.net_worth += 2 * cost
                case 3:
                    cost = board.map[best_location].downgrade_hotel_to_houses()
                    self.lose_money(cost)
                    self.net_worth += 8 * cost
                case 4:
                    self.gain_money(board.map[best_location].mortgage())
                case 5:
                    self.lose_money(board.map[best_location].unmortgage())

if __name__ == '__main__':
    board = Board()
    player1 = Agent('player1')
    player2 = Agent('player2')
    board.map[13].owner = player2
    board.map[19].owner = player2
    board.map[16].owner = player1
    player2.location = 10
    score = player2.get_jail_heuristic(player1, 1, board, False)