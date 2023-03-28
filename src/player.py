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
        self.name = name
        self.turns = 0
    
    def is_bankrupt(self) -> bool:
        return self.money <= 0
    
    def get_money(self) -> int:
        return self.money
    
    def lose_money(self, money: int) -> None:
        self.money -= money
        self.net_worth -= money
        # print_with_color(f'{self.name} lost {money}$ cash.', self)
    
    def gain_money(self, money: int) -> None:
        self.money += money
        self.net_worth += money
        # print_with_color(f'{self.name} gained {money}$ cash.', self)

    def move(self, places: int) -> int:
        previous_location = self.location
        self.location += places
        if self.location >= 40:
            self.gain_money(200) # A player who lands on or passes the "Go" space collects $200 from the bank.
            print_with_color(f'{self.name} collected 200$ by passing GO!', self)
            self.location %= 40
        print_with_color(f'{self.name} moved from {previous_location} to {self.location}.', self)
        return self.location

    def go_to_jail(self) -> None:
        self.location = 10
        self.in_jail_counter += 1
        print_with_color(f'{self.name} went to jail.', self)
    
    def jail_times_increment(self) -> int:
        self.in_jail_counter += 1
        print_with_color(f'{self.name}\'s in jail {self.in_jail_counter} turns in a row.', self)
        return self.in_jail_counter

    def is_in_jail(self) -> bool:
        return self.in_jail_counter > 0
    
    def get_out_of_jail(self) -> None:
        self.in_jail_counter = 0
        print_with_color(f'{self.name} just got out of jail.', self)

    def jail_decide(self, dice: Dice) -> bool:
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
                return False
        return True
    
    def check_has_all_in_color_set(self, color: str) -> bool:
        if color == 'brown' or color == 'dark blue':
            return len(self.properties[color]) == 2
        return len(self.properties[color]) == 3

    def buy(self, item) -> int:
        self.lose_money(item.cost)
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
        return item.cost

    def pay_rent(self, rent: int, other_player=None, item=None) -> None:
        self.lose_money(rent)
        if other_player != None:
            other_player.gain_money(rent)
            print_with_color(f'{self.name} paid {rent}$ rent to {other_player.name} for landing on {item}.', self)
        else:
            print_with_color(f'{self.name} paid {rent}$ rent to bank.', self)
    
    def buy_or_not(self, item) -> int:
        buy = input(f'Buy {item}?[y/N] ')
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
    
    def get_destroyable_properties_on_color_set(self, color: str):
        if self.properties[color][0].number_of_houses == self.properties[color][1].number_of_houses == self.properties[color][2].number_of_houses == 0:
            return
        if self.properties[color][0].number_of_houses == self.properties[color][1].number_of_houses == self.properties[color][2].number_of_houses:
                yield self.properties[color][0]
                yield self.properties[color][1]
                yield self.properties[color][2]
        elif self.properties[color][0].number_of_houses >= self.properties[color][1].number_of_houses == self.properties[color][2].number_of_houses:
                yield self.properties[color][0]
        elif self.properties[color][1].number_of_houses >= self.properties[color][0].number_of_houses == self.properties[color][2].number_of_houses:
                yield self.properties[color][1]
        elif self.properties[color][2].number_of_houses >= self.properties[color][0].number_of_houses == self.properties[color][1].number_of_houses:
                yield self.properties[color][2]
    
    def build_or_not(self):
        color_sets = ['brown', 'light blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark blue']
        available_color_sets = []
        for color in color_sets:
            if self.check_has_all_in_color_set(color):
                available_color_sets.append(color)
        for color in available_color_sets:
            # print_with_color(f'speaking of {color} set...', self)
            for prop in self.get_buildable_properties_on_color_set(color):
                build_house_on_property = input(f'Build house on property {prop}?[y/N] ')
                if build_house_on_property == 'y':
                    cost = prop.build_house()
                    self.lose_money(cost)
                    self.net_worth += cost / 2.0
                    print_with_color(f'{self.name} paid {cost}$ for {prop}.', self)
            for prop in self.properties[color]:
                if prop.get_number_of_houses() == 4 and Property.get_available_hotels() > 0:
                    upgrade_to_hotel = input(f'Upgrade houses in {prop} to a hotel?[y/N] ')
                    if upgrade_to_hotel == 'y':
                        cost = prop.upgrade_houses_to_hotel()
                        self.lose_money(cost)
                        self.net_worth += 2 * cost
                        print_with_color(f'{self.name} upgraded houses on {prop} to a hotel for {cost}$.', self)
                if prop.get_number_of_hotels() == 1 and Property.get_available_houses() > 3:
                    downgrade_to_hotel = input(f'Downgrade hotel in {prop} to 4 houses?[y/N] ')
                    if downgrade_to_hotel == 'y':
                        cost = prop.downgrade_hotel_to_houses()
                        self.lose_money(cost)
                        self.net_worth += 8 * cost
                        print_with_color(f'{self.name} downgraded the hotel on {prop} to 4 houses for {cost}$.')

    def destroy_or_not(self): # sell buildings
        color_sets = ['brown', 'light blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark blue']
        available_color_sets = []
        for color in color_sets:
            if self.check_has_all_in_color_set(color):
                available_color_sets.append(color)
        for color in available_color_sets:
            # print_with_color(f'speaking of {color} set...', self)
            for prop in self.get_destroyable_properties_on_color_set(color):
                destroy_house_on_property = input(f'Destroy house on {prop}?[y/N] ')
                if destroy_house_on_property == 'y':
                    cash = prop.destroy_house()
                    self.gain_money(cash)
                    self.net_worth -= cash * 2
                    print_with_color(f'{self.name} sold a house on {prop} for {cash}$.', self)

    def mortgage_or_not(self):
        for props in self.properties.values():
            for prop in props:
                if not prop.is_mortgaged and prop.number_of_houses == 0 and prop.number_of_hotels == 0:
                    to_mortgage = input(f'Mortgage {prop}? [y/N] ')
                    if to_mortgage == 'y':
                        self.gain_money(prop.mortgage())
        for railroad in self.railroads:
            if not railroad.is_mortgaged:
                to_mortgage = input(f'Mortgage {railroad}? [y/N] ')
                if to_mortgage == 'y':
                    self.gain_money(railroad.mortgage())
        for util in self.utilities:
            if not util.is_mortgaged:
                to_mortgage = input(f'Mortgage {util}? [y/N] ')
                if to_mortgage == 'y':
                    self.gain_money(util.mortgage())
    
    def unmortgage_or_not(self):
        for prop in self.properties.values():
            if prop.is_mortgaged:
                to_mortgage = input(f'Unmortgage {prop}? [y/N] ')
                if to_mortgage == 'y':
                    self.lose_money(prop.mortgage())
        for railroad in self.railroads:
            if railroad.is_mortgaged:
                to_mortgage = input(f'Unmortgage {railroad}? [y/N] ')
                if to_mortgage == 'y':
                    self.lose_money(railroad.mortgage())
        for util in self.utilities:
            if util.is_mortgaged:
                to_mortgage = input(f'Unmortgage {util}? [y/N] ')
                if to_mortgage == 'y':
                    self.lose_money(util.mortgage())

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
                cost = self.buy_or_not(item)
                if cost != -1:
                    print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner() != self and not item.is_mortgaged:
                self.pay_rent(item.get_rent(), item.get_owner(), item)
        elif isinstance(item, Railroad):
            if item.get_owner() is None:
                cost = self.buy_or_not(item)
                if cost != -1:
                    print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner() != self and not item.is_mortgaged:
                self.pay_rent(2 ** (item.get_owner().get_number_of_railroads() - 1) * 25, item.get_owner(), item)
        elif isinstance(item, Utility):
            if item.get_owner() is None:
                cost = self.buy_or_not(item)
                if cost != -1:
                    print_with_color(f'{self.name} bought {item} for {cost}$.', self)
            elif item.get_owner() != self and not item.is_mortgaged:
                if item.get_owner().get_number_of_utilities() == 1:
                    self.pay_rent(dice.get_places() * 4, item.get_owner(), item)
                else: # owner's number of utilities is 2
                    self.pay_rent(dice.get_places() * 10, item.get_owner(), item)
        elif isinstance(item, int):
            self.pay_rent(item)

    def display(self) -> None:
        print_with_color(f'============ player {self.name} ===========', self)
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
    
    def turn(self, other_player, board: Board, dice: Dice):
        # self.display()
        self.turns += 1
        if self.is_in_jail():
            if not self.jail_decide(dice):
                self.build_or_not()
                self.destroy_or_not()
                self.mortgage_or_not()
                return
        dice.roll(self)
        self.action(board, dice)
        self.build_or_not()
        self.destroy_or_not()
        self.mortgage_or_not()