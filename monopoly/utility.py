# from player import Player

class Utility:
    def __init__(self, name: str):
        self.name = name
        self.cost = 150
        self.owner = None
    
    def set_owner(self, owner) -> None:
        self.owner = owner
    
    def get_owner(self):
        return self.owner
    
    def __repr__(self) -> str:
        return f'{self.name}, cost: {self.cost}$'