class Player:
    def __init__(self) -> None:
        self.money = 1500
        self.location = 0
        self.in_jail_counter = 0
    
    def move(self, places: int) -> int:
        self.location += places
        if self.location >= 40:
            self.money += 200 # A player who lands on or passes the "Go" space collects $200 from the bank.
            self.location %= 40
        return self.location

    def go_to_jail(self) -> None:
        self.location = 10
        self.in_jail_counter += 1

    def is_in_jail(self) -> bool:
        return self.in_jail_counter > 0