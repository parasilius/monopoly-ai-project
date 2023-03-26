from property import Property
from railroad import Railroad
from utility import Utility

class Board:
    def __init__(self):
        properties = [
            # cost, site, rent w/ 1 house, rent w/ 2 houses, rent w/ 3 houses, rent w/ 4 houses, hotel
            ['Mediterranean Avenue', 'brown', 60, 2, 10, 30, 90, 160, 250], # Mediterranean Avenue (brown set)
            ['Baltic Avenue', 'brown', 60, 4, 20, 60, 180, 320, 450], # Baltic Avenue	(brown set)
            ['Oriental AvenueBaltic Avenue', 'light blue', 100, 6, 30, 90, 270, 400, 550], # Oriental Avenue (light blue set)
            ['Vermont Avenue', 'light blue', 100, 6, 30, 90, 270, 400, 550], # Vermont Avenue (light blue set)
            ['Connecticut Avenue', 'light blue', 120, 8, 40, 100, 300, 450, 600], # Connecticut Avenue (light blue set)
            ['St. Charles Place', 'pink', 140, 10, 50, 150, 450, 625, 750], # St. Charles Place (pink set)
            ['States Avenue', 'pink', 140, 10, 50, 150, 450, 625, 750], # States Avenue (pink set)
            ['Virginia Avenue', 'pink', 160, 12, 60, 180, 500, 700, 900], # Virginia Avenue (pink set)
            ['St. James Place', 'orange', 180, 14, 70, 200, 550, 750, 950], # St. James Place (orange set)
            ['Tennessee Avenue', 'orange', 180, 14, 70, 200, 550, 750, 950], # Tennessee Avenue (orange set)
            ['New York Avenue', 'orange', 200, 16, 80, 220, 600, 800, 1000], # New York Avenue (orange set)
            ['Kentucky Avenue', 'red', 220, 18, 90, 250, 700, 875, 1050], # Kentucky Avenue (red set)
            ['Indiana Avenue', 'red', 220, 18, 90, 250, 700, 875, 1050], # Indiana Avenue (red set)
            ['Illinois Avenue', 'red', 240, 20, 100, 300, 750, 925, 1100], # Illinois Avenue (red set)
            ['Atlantic Avenue', 'yellow', 260, 22, 110, 330, 800, 975, 1150], # Atlantic Avenue (yellow set)
            ['Ventnor Avenue', 'yellow', 260, 22, 110, 330, 800, 975, 1150], # Ventnor Avenue (yellow set)
            ['Marvin Gardens', 'yellow', 280, 24, 120, 360, 850, 1025, 1200], # Marvin Gardens (yellow set)
            ['Pacific Avenue', 'green', 300, 26, 130, 390, 900, 1100, 1275], # Pacific Avenue (green set)
            ['North Carolina Avenue', 'green', 300, 26, 130, 390, 900, 1100, 1275], # North Carolina Avenue (green set)
            ['North Carolina Avenue', 'green', 320, 28, 150, 450, 1000, 1200, 1400], # North Carolina Avenue (green set)
            ['Park Place', 'dark blue', 350, 35, 175, 500, 1100, 1300, 1500], # Park Place (dark blue set)
            ['Boardwalk', 'dark blue', 400, 50, 200, 600, 1400, 1700, 2000] # Boardwalk (dark blue set)
        ]

        def property_locations():
            yield 1
            yield 3
            yield 6
            yield 8
            yield 9
            yield 11
            yield 13
            yield 14
            yield 16
            yield 18
            yield 19
            yield 21
            yield 23
            yield 24
            yield 26
            yield 27
            yield 29
            yield 31
            yield 32
            yield 34
            yield 37
            yield 39

        self.map = [None] * 40
        i = 0
        for idx in property_locations():
            print(idx)
            self.map[idx] = Property(properties[i][0], properties[i][1], properties[i][2], properties[i][3:])
            i += 1

        def railroad_names():
            yield 'Reading Railroad'
            yield 'Pennsylvania Railroad'
            yield 'B. & O. Railroad'
            yield 'Short Line'
        i = 0
        for name in railroad_names():
            self.map[i * 10 + 5] = Railroad(name)
            i += 1
        
        self.map[12] = Utility('Electric Company')
        self.map[28] = Utility('Water Works')

        self.map[4] = 200 # Income Tax
        self.map[38] = 100 # Luxury Tax
    def get_item_at_location(self, location: int):
        return self.map[location]