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
            self.map[idx] = Property(properties[i][0], properties[i][1], properties[i][2], properties[i][3:])
            self.map[idx].lprobability = lprobabilities[i]
            self.map[idx].sprobability = sprobabilities[i]
            i += 1
       
        i = 0
        for name in railroad_names():
            self.map[i * 10 + 5] = Railroad(name)
            self.map[i * 10 + 5].lprobability = lprobabilities[i * 10 + 5]
            self.map[i * 10 + 5].sprobability = sprobabilities[i * 10 + 5]
            i += 1
        
        self.map[12] = Utility('Electric Company')
        self.map[12].lprobability = lprobabilities[12]
        self.map[12].sprobability = sprobabilities[12]
        self.map[28] = Utility('Water Works')
        self.map[28].lprobability = lprobabilities[28]
        self.map[28].sprobability = sprobabilities[28]

        self.map[4] = Square(200, lprobabilities[4], sprobabilities[4]) # Income Tax
        self.map[38] = Square(100, lprobabilities[38], sprobabilities[38]) # Luxury Tax

    def get_item_at_location(self, location: int):
        return self.map[location]
