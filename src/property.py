# from player import Player
from utilities import *
from square import Square

building_costs = {
    'brown': 50,
    'light blue': 50,
    'pink': 100,
    'orange': 100,
    'red': 150,
    'yellow': 150,
    'green': 200,
    'dark blue': 200
}

number_of_mortgaged_properties_in_color_set = {
    'brown': 0,
    'light blue': 0,
    'pink': 0,
    'orange': 0,
    'red': 0,
    'yellow': 0,
    'green': 0,
    'dark blue': 0
}

class Property(Square):
    available_houses = 32
    available_hotels = 12

    @classmethod
    def add_houses(num: int) -> int:
        if Property.available_houses + num > 32:
            return -1
        Property.available_houses += num
        return Property.available_houses

    @classmethod
    def remove_houses(num: int) -> int:
        if Property.available_houses - num < 0:
            return -1
        Property.available_houses -= num
        return Property.available_houses

    @classmethod
    def add_hotels(num: int) -> int:
        if Property.available_hotels + num > 12:
            return -1
        Property.available_hotels += num
        return Property.available_hotels

    @classmethod
    def remove_hotels(num: int) -> int:
        if Property.available_hotels - num < 12:
            return -1
        Property.available_hotels += num
        return Property.available_hotels
    
    @classmethod
    def get_available_houses() -> int:
        return Property.available_houses
    
    @classmethod
    def get_available_hotels() -> int:
        return Property.available_hotels

    def __init__(self, name, color, cost, rents):
        self.name = name
        self.color = color
        self.cost = cost
        self.rents = rents
        self.number_of_hotels = 0
        self.number_of_houses = 0
        self.is_mortgaged = False
        self.mortgage_value = cost / 2.0
        self.owner = None
        self.has_all_in_color_set = False
        self.building_price = building_costs[color]
        global number_of_mortgaged_properties_in_color_set
    
    def set_owner(self, owner) -> None:
        self.owner = owner
    
    def get_owner(self):
        return self.owner

    def get_number_of_houses(self) -> int:
        return self.number_of_houses

    def get_number_of_hotels(self) -> int:
        return self.number_of_hotels

    def mortgage(self) -> int:
        self.is_mortgaged = True
        number_of_mortgaged_properties_in_color_set[self.color] += 1
        return self.mortgage_value

    def unmortgage(self) -> int:
        self.is_mortgaged = False
        number_of_mortgaged_properties_in_color_set[self.color] -= 1
        return 1.1 * self.mortgage_value
    
    def get_rent(self) -> int:
        if self.has_all_in_color_set:
            if self.number_of_houses > 0:
                return self.rents[self.number_of_houses]
            elif self.number_of_hotels > 0:
                return self.rents[5]
            else:
                return self.rents[0] * 2
        else:
            return self.rents[0]
    
    def can_build_house(self) -> bool:
        return self.number_of_houses < 4 and self.has_all_in_color_set and number_of_mortgaged_properties_in_color_set[self.color] == 0
    
    def build_house(self) -> int:
        self.number_of_houses += 1
        Property.available_houses -= 1
        return self.building_price
    
    def destroy_house(self) -> int:
        self.number_of_houses -= 1
        Property.available_houses += 1
        return self.building_price / 2.0

    def upgrade_houses_to_hotel(self) -> int:
        if self.number_of_houses == 4 and Property.available_hotels > 0:
            self.number_of_houses = 0
            self.number_of_hotels = 1
            Property.available_hotels -= 1
            Property.available_houses += 4
            return self.building_price
        return -1
    
    def downgrade_hotel_to_houses(self) -> int:
        if self.number_of_hotels == 1 and Property.available_houses >= 4:
            self.number_of_houses = 4
            self.number_of_hotels = 0
            Property.available_hotels += 1
            Property.available_houses -= 4
            return self.building_price / 2.0
        return -1

    def display(self, player):
        print_with_color('------------', player)
        print_with_color(f'{self.name}', player)
        print_with_color(f'rent {self.rents[0]}$, w/1x🏠:{self.rents[1]}$, w/2x🏠:{self.rents[2]}, w/3x🏠:{self.rents[3]}$, w/4x🏠:{self.rents[4]}$, w/1x🏨:{self.rents[5]}$', player)
        print_with_color(f'buildings cost {self.building_price}$', player)
        for _ in range(self.number_of_houses):
            print_with_color('🏠', player)
        for _ in range(self.number_of_hotels):
            print_with_color('🏨', player)
        print_with_color('------------', player)
    
    def __repr__(self) -> str:
        return f'{self.name}'
