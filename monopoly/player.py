from property import Property
from utilities import *

class Player:
    def __init__(self, name: str) -> None:
        self.money = 1500
        self.location = 0
        self.in_jail_counter = 0
        self.properties = {}
        self.number_of_railroads = 0
        self.number_of_utilities = 0
        self.player_name = name
        self.is_bankrupt = False
    
    def get_money(self) -> int:
        return self.money
    
    def lose_money(self, money: int) -> None:
        if self.money > money:
            self.money -= money
        else:
            self.money = 0
            self.is_bankrupt = True
    
    def gain_money(self, money: int) -> None:
        self.money += money

    def move(self, places: int) -> int:
        previous_location = self.location
        self.location += places
        if self.location >= 40:
            self.money += 200 # A player who lands on or passes the "Go" space collects $200 from the bank.
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
    
    def check_has_all_in_color_set(self, color: str) -> bool:
        if color not in self.properties:
            return False
        if color == 'brown' or color == 'dark blue':
            return len(self.properties[color]) == 2
        return len(self.properties[color]) == 3

    def buy(self, item) -> int:
        self.money -= item.cost
        item.set_owner(self)
        if isinstance(item, Property) and item.color in self.properties:
            self.properties[item.color].append(item)
            if self.check_has_all_in_color_set(item.color):
                for owned_property in self.properties[item.color]:
                    owned_property.has_all_in_color_set = True

    def pay_rent(self, rent: int, other_player=None) -> None:
        if self.money >= rent:
            self.money -= rent
            if other_player != None:
                other_player.gain_money(rent)
                print_with_color(f'player {self.player_name} paid {rent}$ rent to {other_player.player_name}.', self)
            else:
                print_with_color(f'player {self.player_name} paid {rent}$ rent to bank.', self)
        else:
            self.money = 0
    
    def build(self, prop) -> bool:
        house_price = prop.build_house()
        if house_price != -1:
            self.money -= house_price
            return True
        else:
            return False

    def buy_or_not(self, item) -> int:
        if self.money >= item.cost:
            buy = input('Buy property? [y/n] ')
            if buy == 'y':
                return self.buy(item)
            elif buy == 'n':
                return -1
    
    def get_buildable_properties_on_color_set(self, color: str):
        if self.properties[color][0] == self.properties[color][1] == self.properties[color][2]:
            if self.money >= self.properties[color][0].building_price and self.properties[color][0].available_houses > 0 and self.properties[color][0].can_build_house():
                yield self.properties[color][0]
            if self.money >= self.properties[color][1].building_price and self.properties[color][1].available_houses > 0 and self.properties[color][1].can_build_house():
                yield self.properties[color][1]
            if self.money >= self.properties[color][2].building_price and self.properties[color][2].available_houses > 0 and self.properties[color][2].can_build_house():
                yield self.properties[color][2]
        elif self.properties[color][0] >= self.properties[color][1] == self.properties[color][2]:
            if self.money >= self.properties[color][1].building_price and self.properties[color][1].available_houses > 0 and self.properties[color][1].can_build_house():
                yield self.properties[color][1]
            if self.money >= self.properties[color][2].building_price and self.properties[color][2].available_houses > 0 and self.properties[color][2].can_build_house():
                yield self.properties[color][2]
        elif self.properties[color][1] >= self.properties[color][0] == self.properties[color][2]:
            if self.money >= self.properties[color][0].building_price and self.properties[color][0].available_houses > 0 and self.properties[color][0].can_build_house():
                yield self.properties[color][0]
            if self.money >= self.properties[color][2].building_price and self.properties[color][2].available_houses > 0 and self.properties[color][2].can_build_house():
                yield self.properties[color][2]
        elif self.properties[color][2] >= self.properties[color][0] == self.properties[color][1]:
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
                print_with_color(f'speaking of {self.properties[color]}...', self)
                if len(self.properties[color]) == 3:
                    for prop in self.get_buildable_properties_on_color_set(color):
                        build_house_on_property = input(f'Build house on property {prop}?[y/N] ')
                        if build_house_on_property == 'y':
                            self.lose_money(prop.build_house())
                for prop in self.properties[color]:
                    if prop.get_number_of_houses() == 4 and prop.get_available_hotels() > 0:
                        upgrade_to_hotel = input(f'Upgrade houses in {prop} to a hotel?[y/N] ')
                        if upgrade_to_hotel == 'y':
                            self.lose_money(prop.upgrade_houses_to_hotel())
                    if prop.get_number_of_hotels() == 1 and prop.get_available_houses() > 3:
                        downgrade_to_hotel = input(f'Downgrade hotel in {prop} to 4 houses?[y/N] ')
                        if downgrade_to_hotel == 'y':
                            self.lose_money(prop.downgrade_houses_to_hotel())
    
    def get_number_of_railroads(self) -> int:
        return self.number_of_railroads
    
    def get_number_of_utilities(self) -> int:
        return self.number_of_utilities
    
    def display_info(self) -> None:
        print('=========================')
        print(f'============ player {self.player_id} ===========')
        print('\t==== properties =====')
        for color in self.properties:
            print(f'\t==== {color} set ====')
            for property in self.properties[color]:
                property.display_info()