from property import Property
from railroad import Railroad
from utility import Utility
from board import Board
from dice import Dice
from utilities import *

class Player:
    def __init__(self, name: str) -> None:
        self.money = 1500
        self.net_worth = 1500
        self.location = 0
        self.in_jail_counter = 0
        self.properties = {
            'brown': [],
            'light blue': [],
            'pink': [],
            'orange': [],
            'red': [],
            'yellow': [],
            'green': [],
            'dark blue': []
        }
        self.railroads = []
        self.utilities = []
        self.player_name = name
        self.turns = 0
    
    def is_bankrupt(self) -> bool:
        return self.money <= 0
    
    def get_money(self) -> int:
        return self.money
    
    def lose_money(self, money: int) -> None:
        self.money -= money
        self.net_worth -= money
        print_with_color(f'player {self.player_name} lost {money}$ cash.', self)
    
    def gain_money(self, money: int) -> None:
        self.money += money
        self.net_worth += money
        print_with_color(f'player {self.player_name} gained {money}$ cash.', self)

    def move(self, places: int) -> int:
        previous_location = self.location
        self.location += places
        if self.location >= 40:
            self.gain_money(200) # A player who lands on or passes the "Go" space collects $200 from the bank.
            print_with_color(f'player {self.player_name} collected 200$ by passing GO!', self)
            self.location %= 40
        print_with_color(f'player {self.player_name} moved from {previous_location} to {self.location}.', self)
        return self.location

    def go_to_jail(self) -> None:
        self.location = 10
        self.in_jail_counter += 1
        print_with_color(f'player {self.player_name} went to jail.', self)
    
    def jail_times_increment(self) -> int:
        self.in_jail_counter += 1
        print_with_color(f'player {self.player_name}\'s in jail {self.in_jail_counter} turns in a row.', self)
        return self.in_jail_counter

    def is_in_jail(self) -> bool:
        return self.in_jail_counter > 0
    
    def get_out_of_jail(self) -> None:
        self.in_jail_counter = 0
        print_with_color(f'player {self.player_name} just got out of jail.', self)

    def jail_decide(self, dice: Dice) -> None:
        check = input('Give 50$ to get out of jail? [y/N] ')
        if check == 'y':
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
    
    def check_has_all_in_color_set(self, color: str) -> bool:
        if color == 'brown' or color == 'dark blue':
            return len(self.properties[color]) == 2
        return len(self.properties[color]) == 3

    def buy(self, item) -> int:
        self.lose_money(item.cost)
        self.net_worth += item.cost
        item.set_owner(self)
        if isinstance(item, Property):
            self.properties[item.color].append(item)
            if self.check_has_all_in_color_set(item.color):
                for owned_property in self.properties[item.color]:
                    owned_property.has_all_in_color_set = True
        elif isinstance(item, Railroad):
            self.railroads.append(item)
        elif isinstance(item, Utility):
            self.utilities.append(item)

    def pay_rent(self, rent: int, other_player=None) -> None:
        if self.money >= rent:
            self.lose_money(rent)
            if other_player != None:
                other_player.gain_money(rent)
                print_with_color(f'player {self.player_name} paid {rent}$ rent to {other_player.player_name}.', self)
            else:
                print_with_color(f'player {self.player_name} paid {rent}$ rent to bank.', self)
        else:
            self.money = 0
    
    def build(self, prop) -> bool:
        house_price = prop.build_house()
        self.net_worth += prop.building_price
        if house_price != -1:
            self.lose_money(house_price)
            return True
        return False

    def buy_or_not(self, item) -> int:
        buy = input('Buy property? [y/n] ')
        if buy == 'y':
            return self.buy(item)
        return -1
    
    def get_buildable_properties_on_color_set(self, color: str):
        if self.properties[color][0].number_of_houses == self.properties[color][1].number_of_houses == self.properties[color][2].number_of_houses:
            if self.money >= self.properties[color][0].building_price and self.properties[color][0].available_houses > 0 and self.properties[color][0].can_build_house():
                yield self.properties[color][0]
            if self.money >= self.properties[color][1].building_price and self.properties[color][1].available_houses > 0 and self.properties[color][1].can_build_house():
                yield self.properties[color][1]
            if self.money >= self.properties[color][2].building_price and self.properties[color][2].available_houses > 0 and self.properties[color][2].can_build_house():
                yield self.properties[color][2]
        elif self.properties[color][0].number_of_houses >= self.properties[color][1].number_of_houses == self.properties[color][2].number_of_houses:
            if self.money >= self.properties[color][1].building_price and self.properties[color][1].available_houses > 0 and self.properties[color][1].can_build_house():
                yield self.properties[color][1]
            if self.money >= self.properties[color][2].building_price and self.properties[color][2].available_houses > 0 and self.properties[color][2].can_build_house():
                yield self.properties[color][2]
        elif self.properties[color][1].number_of_houses >= self.properties[color][0].number_of_houses == self.properties[color][2].number_of_houses:
            if self.money >= self.properties[color][0].building_price and self.properties[color][0].available_houses > 0 and self.properties[color][0].can_build_house():
                yield self.properties[color][0]
            if self.money >= self.properties[color][2].building_price and self.properties[color][2].available_houses > 0 and self.properties[color][2].can_build_house():
                yield self.properties[color][2]
        elif self.properties[color][2].number_of_houses >= self.properties[color][0].number_of_houses == self.properties[color][1].number_of_houses:
            if self.money >= self.properties[color][0].building_price and self.properties[color][0].available_houses > 0 and self.properties[color][0].can_build_house():
                yield self.properties[color][0]
            if self.money >= self.properties[color][1].building_price and self.properties[color][1].available_houses > 0 and self.properties[color][1].can_build_house():
                yield self.properties[color][1]
    
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
                print_with_color(f'speaking of {color} set...', self)
                if len(self.properties[color]) == 3:
                    for prop in self.get_buildable_properties_on_color_set(color):
                        build_house_on_property = input(f'Build house on property {prop}?[y/N] ')
                        if build_house_on_property == 'y':
                            self.lose_money(prop.build_house())
                for prop in self.properties[color]:
                    if prop.get_number_of_houses() == 4 and Property.get_available_hotels() > 0:
                        upgrade_to_hotel = input(f'Upgrade houses in {prop} to a hotel?[y/N] ')
                        if upgrade_to_hotel == 'y':
                            self.lose_money(prop.upgrade_houses_to_hotel())
                    if prop.get_number_of_hotels() == 1 and Property.get_available_houses() > 3:
                        downgrade_to_hotel = input(f'Downgrade hotel in {prop} to 4 houses?[y/N] ')
                        if downgrade_to_hotel == 'y':
                            self.lose_money(prop.downgrade_houses_to_hotel())
    
    def sell_or_not(self):
        pass
    
    def get_number_of_railroads(self) -> int:
        return len(self.railroads)
    
    def get_number_of_utilities(self) -> int:
        return len(self.utilities)

    def action(self, board: Board, dice: Dice):
        location = self.move(dice.get_places())
        item = board.get_item_at_location(location)
        if location == 30:
            self.go_to_jail()
        elif isinstance(item, Property):
            if item.get_owner() is None:
                self.buy_or_not(item)
            elif item.get_owner() != self:
                self.pay_rent(item.get_rent(), item.get_owner())
        elif isinstance(item, Railroad):
            if item.get_owner() is None:
                self.buy_or_not(item)
            elif item.get_owner() != self:
                self.pay_rent(2 ** (item.get_owner().get_number_of_railroads() - 1) * 25, item.get_owner())
        elif isinstance(item, Utility):
            if item.get_owner() is None:
                self.buy_or_not(item)
            elif item.get_owner() != self:
                if item.get_owner().get_number_of_utilities() == 1:
                    self.pay_rent(dice.get_places() * 4, item.get_owner())
                else: # owner's number of utilities is 2
                    self.pay_rent(dice.get_places() * 10, item.get_owner())
        elif isinstance(item, int):
            self.pay_rent(item)

    def display(self) -> None:
        print_with_color(f'============ player {self.player_name} ===========', self)
        print_with_color(f'money: {self.money}', self)
        print_with_color('\t==== properties =====', self)
        for color in self.properties:
            print_with_color(f'\t==== {color} set ====', self)
            for property in self.properties[color]:
                property.display(self)
        print_with_color('\t==== railroads  =====', self)
        for railroad in self.railroads:
            print_with_color(railroad, self)
        print_with_color('\t==== utilities  =====', self)
        for utility in self.utilities:
            print_with_color(utility, self)
    
    def turn(self, board: Board, dice: Dice):
        self.display()
        if self.is_in_jail():
            self.jail_decide(dice)
        dice.roll(self)
        self.action(board, dice)
        self.build_or_not()
        self.turns += 1