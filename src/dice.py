from random import randint
from utilities import *

class Dice:
    def __init__(self) -> None:
        self.first = None
        self.second = None
        self.double_counter = 0

    def roll(self, player) -> None:
        self.die1 = randint(1, 6)
        self.die2 = randint(1, 6)
        print_with_color(f'die 1: {self.die1}, die 2: {self.die2}', player)
    
    def get_places(self) -> int:
        return self.die1 + self.die2
    
    def is_double(self) -> bool:
        return self.die1 == self.die2