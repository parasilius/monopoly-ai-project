from player import Player
from property import Property
from dice import Dice
import random
from utilities import *

class RandomAgent(Player):
    def buy_or_not(self, item) -> int:
        if bool(random.getrandbits(1)):
            return self.buy(item)
        return -1
    
    def build_or_not(self):
        for prop in self.get_buildable_properties():
            if bool(random.getrandbits(1)):
                cost = prop.build_house()
                self.lose_money(cost)
                self.net_worth += cost / 2.0
                break

    def upgrade_houses_or_not(self):
        for prop in self.get_buildable_properties():
            if prop.get_number_of_houses() == 4:
                if bool(random.getrandbits(1)):
                    cost = prop.upgrade_houses_to_hotel()
                    self.lose_money(cost)
                    self.net_worth += 2 * cost
                    break
 
    def downgrade_hotel_or_not(self):
        for prop in self.get_downgradable_properties():
            if bool(random.getrandbits(1)):
                cost = prop.downgrade_hotel_to_houses()
                self.lose_money(cost)
                self.net_worth += 8 * cost
                break

    def jail_decide(self):
        if bool(random.getrandbits(1)):
            self.lose_money(50)
            self.get_out_of_jail()

    def mortgage_or_not(self):
        for prop in self.get_properties():
            if not prop.is_mortgaged and prop.number_of_houses == 0 and prop.number_of_hotels == 0:
                if bool(random.getrandbits(1)):
                    self.gain_money(prop.mortgage())
                    break
        for railroad in self.railroads:
            if not railroad.is_mortgaged:
                if bool(random.getrandbits(1)):
                    self.gain_money(railroad.mortgage())
                    break
        for util in self.utilities:
            if not util.is_mortgaged:
                if bool(random.getrandbits(1)):
                    self.gain_money(util.mortgage())
                    break

    def unmortgage_or_not(self):
        for prop in self.get_properties():
            if prop.is_mortgaged:
                if bool(random.getrandbits(1)):
                    self.lose_money(prop.unmortgage())
                    break
        for railroad in self.railroads:
            if railroad.is_mortgaged:
                if bool(random.getrandbits(1)):
                    self.lose_money(railroad.unmortgage())
                    break
        for util in self.utilities:
            if util.is_mortgaged:
                if bool(random.getrandbits(1)):
                    self.lose_money(util.unmortgage())
                    break
 
    def destroy_or_not(self): # sell buildings
        for prop in self.get_destroyable_properties():
            if bool(random.getrandbits(1)):
                cash = prop.destroy_house()
                self.gain_money(cash)
                self.net_worth -= cash * 2
                print_with_color(f'{self.name} sold a house on {prop} for {cash}$.', self)
                break

    def turn(self, other_player, board, dice: Dice):
        # self.display()
        self.turns += 1
        if self.is_in_jail():
            self.jail_decide()
        dice.roll(self)
        if self.is_in_jail() and (dice.is_double() or self.jail_times_increment() > 2):
            self.lose_money(50)
            self.get_out_of_jail()
        if not self.is_in_jail():
            self.action(board, dice)
        num = random.randint(1, 6)
        match num:
            case 1:
                self.build_or_not()
            case 2:
                self.destroy_or_not()
            case 3:
                self.upgrade_houses_or_not()
            case 4:
                self.downgrade_hotel_or_not()
            case 5:
                self.mortgage_or_not()
            case 6:
                self.unmortgage_or_not()