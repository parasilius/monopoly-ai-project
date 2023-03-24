class Property:
    def __init__(self, color, cost, rents):
        self.color = color
        self.cost = price
        self.rents = rents
        self.number_of_hotels = 0
        self.number_of_houses = 0
        self.is_mortgaged = False
        self.mortgage_value = price / 2
    
    def set_owner(self, owner: Player) -> None:
        self.owner = owner
    
    def get_owner(self) -> Player:
        return self.owner

    def mortgage(self) -> int:
        if not self.is_mortgaged:
            self.is_mortgaged = True
            return self.mortgage_value
        else:
            print('Error: Property is already mortgaged!')
            return -1

    def unmortgage(self) -> int:
        if self.is_mortgaged:
            self.is_mortgaged = False
            return self.mortgage_value + 1.1 * self.mortgage_value
        else:
            print('Error: Property is not mortgaged!')
            return -1