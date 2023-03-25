from player import Player

house_costs = {
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

class Property:
    def __init__(self, color, cost, rents):
        self.color = color
        self.cost = cost
        self.rents = rents
        self.number_of_hotels = 0
        self.number_of_houses = 0
        self.is_mortgaged = False
        self.mortgage_value = cost / 2
        self.owner = None
        self.has_all_in_color_set = False
        self.house_price = house_costs[color]
        global number_of_mortgaged_properties_in_color_set
    
    def set_owner(self, owner: Player) -> None:
        self.owner = owner
    
    def get_owner(self) -> Player:
        return self.owner

    def mortgage(self) -> int:
        if not self.is_mortgaged:
            self.is_mortgaged = True
            number_of_mortgaged_properties_in_color_set[self.color] += 1
            return self.mortgage_value
        else:
            print('Error: Property is already mortgaged!')
            return -1

    def unmortgage(self) -> int:
        if self.is_mortgaged:
            self.is_mortgaged = False
            number_of_mortgaged_properties_in_color_set[self.color] -= 1
            return self.mortgage_value + 1.1 * self.mortgage_value
        else:
            print('Error: Property is not mortgaged!')
            return -1
    
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
    
    def build_house(self) -> int:
        if self.number_of_houses < 5 and self.has_all_in_color_set and number_of_mortgaged_properties_in_color_set[self.color] == 0:
            self.number_of_houses += 1
            return self.house_price
        return -1
    
    def upgrade_houses_to_hotel(self) -> int:
        if self.number_of_houses == 4:
            self.number_of_houses = 0
            self.number_of_hotels = 1
            return self.house_price
        return -1
    
    def display_info(self):
        print('------------')
        for _ in range(self.number_of_houses):
            print('🏠')
        for _ in range(self.number_of_hotels):
            print('🏨')
        print('------------')