from random import randint

class Dices:
    def __init__(self) -> None:
        self.first = None
        self.second = None
        self.double_counter = 0

    def roll(self) -> None:
        self.first = randint(1, 6)
        self.second = randint(1, 6)
        if self.first == self.second:
            self.double_counter += 1
        else:
            self.double_counter = 0
        print(f'dice 1: {self.first}, dice 2: {self.second}')
    
    def get_places(self) -> int:
        return self.first + self.second
    
    def is_double(self) -> bool:
        return self.double_counter > 0

    def get_double_counter(self) -> int:
        return self.double_counter