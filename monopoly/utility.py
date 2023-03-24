class Utility:
    def __init__(self):
        self.cost = 150
    
    def set_owner(self, owner: Player) -> None:
        self.owner = owner
    
    def get_owner(self) -> Player:
        return self.owner