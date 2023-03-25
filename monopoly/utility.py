from player import Player

class Utility:
    def __init__(self):
        self.cost = 150
        self.owner = None
    
    def set_owner(self, owner: Player) -> None:
        self.owner = owner
    
    def get_owner(self) -> Player:
        return self.owner