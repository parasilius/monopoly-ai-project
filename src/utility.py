# from player import Player
from square import Square

class Utility(Square):
    def __init__(self, location, name: str):
        self.name = name
        self.location = location
        self.cost = 150
        self.owner = None
        self.mortgage_value = self.cost / 2.0
        self.is_mortgaged = False
    
    def get_rent(self, dice_places: int) -> int:
        if self.owner.get_number_of_utilities() == 1:
            return dice_places * 4
        else:
            return dice_places * 10
    
    def set_owner(self, owner) -> None:
        self.owner = owner
    
    def get_owner(self):
        return self.owner

    def mortgage(self) -> int:
        self.is_mortgaged = True
        return self.mortgage_value

    def unmortgage(self) -> int:
        self.is_mortgaged = False
        return 1.1 * self.mortgage_value
    
    def __repr__(self) -> str:
        return f'{self.name}'
