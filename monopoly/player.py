class Player:
    def __init__(self, name: str) -> None:
        self.money = 1500
        self.location = 0
        self.in_jail_counter = 0
        self.properties = {}
        self.number_of_railroads = 0
        self.number_of_utilities = 0
        self.player_name = name

    def move(self, places: int) -> int:
        previous_location = self.location
        self.location += places
        if self.location >= 40:
            self.money += 200 # A player who lands on or passes the "Go" space collects $200 from the bank.
            print(f'player {self.player_name} collected 200$ by passing GO!')
            self.location %= 40
        print(f'player {self.player_name} moved from {previous_location} to {self.location}.')
        return self.location

    def go_to_jail(self) -> None:
        self.location = 10
        self.in_jail_counter += 1
    
    def jail_times_increment(self) -> int:
        self.in_jail_counter += 1
        return self.in_jail_counter

    def is_in_jail(self) -> bool:
        return self.in_jail_counter > 0
    
    def get_out_of_jail(self) -> None:
        self.in_jail_counter = 0
        print(f'player {self.player_name} just got out of jail.')
    
    def check_has_all_in_color_set(self, color: str) -> bool:
        if color not in self.properties:
            return False
        if color == 'brown' or color == 'dark blue':
            return len(self.properties[color]) == 2
        return len(self.properties[color]) == 3

    def buy(self, prop) -> int:
        self.money -= prop.cost
        prop.set_owner(self)
        if prop.color in self.properties:
            self.properties[prop.color].append(prop)
            if self.check_has_all_in_color_set(prop.color):
                for owned_property in self.properties[prop.color]:
                    owned_property.has_all_in_color_set = True

    def pay_rent(self, rent: int):
        if self.money >= rent:
            self.money -= rent
            print(f'player {self.player_name} paid {rent}$ rent.')
    
    def build(self, prop) -> bool:
        house_price = prop.build_house()
        if house_price != -1:
            self.money -= house_price
            return True
        else:
            return False

    def buy_or_not(self, prop) -> int:
        if self.money >= prop.cost:
            buy = input('Buy property? [y/n]')
            if buy == 'y':
                return self.buy(prop)
            elif buy == 'n':
                return -1
    
    def build_or_not(self, proprty):
        color_sets = ['brown', 'light blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark blue']
        available_color_sets = []
        for color in color_sets:
            if self.check_has_all_in_color_set(color):
                available_color_sets.append(color)
        if len(available_color_sets) == 0:
            print('You can\'t build any houses!')
        else:
            for color in available_color_sets:
                pass
    
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