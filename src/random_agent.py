from player import Player
from dice import Dice
import random
from utilities import *

class RandomAgent(Player):
    def buy_or_not(self, item) -> int:
        if bool(random.getrandbits(1)):
            return self.buy(item)
        return -1
    
    def build_or_not(self):
        color_sets = ['brown', 'light blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark blue']
        available_color_sets = []
        for color in color_sets:
            if self.check_has_all_in_color_set(color):
                available_color_sets.append(color)
        if len(available_color_sets) == 0:
            print_with_color('You can\'t build any houses!', self)
        else:
            for color in available_color_sets:
                if len(self.properties[color]) == 3:
                    for prop in self.get_buildable_properties_on_color_set(color):
                        if bool(random.getrandbits(1)):
                            self.lose_money(prop.build_house())
                for prop in self.properties[color]:
                    if prop.get_number_of_houses() == 4 and prop.get_available_hotels() > 0:
                        if bool(random.getrandbits(1)):
                            self.lose_money(prop.upgrade_houses_to_hotel())
                    if prop.get_number_of_hotels() == 1 and prop.get_available_houses() > 3:
                        if bool(random.getrandbits(1)):
                            self.lose_money(prop.downgrade_houses_to_hotel())
    
    def jail_decide(self, dice: Dice):
        if bool(random.getrandbits(1)):
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
                return