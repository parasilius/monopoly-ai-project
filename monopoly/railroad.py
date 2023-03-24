class Railroad:
    def __init__(self):
        self.cost = 200
    
    def set_owner(self, owner: Player) -> None:
        self.owner = owner
    
    def get_owner(self) -> Player:
        return self.owner