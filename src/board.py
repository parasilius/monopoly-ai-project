from square import Square
from property import Property
from railroad import Railroad
from utility import Utility
from utilities import *

class Board:
    def __init__(self):
        self.map = [None] * 40
        i = 0
        for idx in property_locations():
            self.map[idx] = Property(idx, properties[i][0], properties[i][1], properties[i][2], properties[i][3:])
            i += 1
       
        i = 0
        for name in railroad_names():
            self.map[i * 10 + 5] = Railroad(i * 10 + 5, name)
            i += 1
        
        self.map[12] = Utility(12, 'Electric Company')
        self.map[28] = Utility(28, 'Water Works')

        self.map[4] = Square(4, 200, lprobabilities[4], sprobabilities[4]) # Income Tax
        self.map[38] = Square(38, 100, lprobabilities[38], sprobabilities[38]) # Luxury Tax

    def get_item_at_location(self, location: int):
        return self.map[location]
