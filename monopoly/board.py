from property import Property
from railroad import Railroad

class Board:
    def __init__(self):
        properties = [
            # cost, site, rent w/ 1 house, rent w/ 2 houses, rent w/ 3 houses, rent w/ 4 houses, hotel
            [60, 2, 10, 30, 90, 160, 250], # Mediterranean Avenue (brown set)
            [60, 4, 20, 60, 180, 320, 450], # Baltic Avenue	(brown set)
            [100, 6, 30, 90, 270, 400, 550], # Oriental Avenue (blue set)
            [100, 6, 30, 90, 270, 400, 550], # Vermont Avenue (blue set)
            [120, 8, 40, 100, 300, 450, 600], # Connecticut Avenue (blue set)
            [140, 10, 50, 150, 450, 625, 750], # St. Charles Place (pink set)
            [140, 10, 50, 150, 450, 625, 750], # States Avenue (pink set)
            [160, 12, 60, 180, 500, 700, 900], # Virginia Avenue (pink set)
            [180, 14, 70, 200, 550, 750, 950], # St. James Place (orange set)
            [180, 14, 70, 200, 550, 750, 950], # Tennessee Avenue (orange set)
            [200, 16, 80, 220, 600, 800, 1000], # New York Avenue (orange set)
            [220, 18, 90, 250, 700, 875, 1050], # Kentucky Avenue (red set)
            [220, 18, 90, 250, 700, 875, 1050], # Indiana Avenue (red set)
            [240, 20, 100, 300, 750, 925, 1100], # Illinois Avenue (red set)
            [260, 22, 110, 330, 800, 975, 1150], # Atlantic Avenue (yellow set)
            [260, 22, 110, 330, 800, 975, 1150], # Ventnor Avenue (yellow set)
            [280, 24, 120, 360, 850, 1025, 1200], # Marvin Gardens (yellow set)
            [300, 26, 130, 390, 900, 1100, 1275], # Pacific Avenue (green set)
            [300, 26, 130, 390, 900, 1100, 1275], # North Carolina Avenue (green set)
            [320, 28, 150, 450, 1000, 1200, 1400], # North Carolina Avenue (green set)
            [350, 35, 175, 500, 1100, 1300, 1500], # Park Place (final set)
            [400, 50, 200, 600, 1400, 1700, 2000] # Boardwalk (final set)
        ]

        self.map = []
        self.map[1] = Property(0, properties[0][0], properties[0][1:])
        self.map[3] = Property(0, properties[1][0], properties[1][1:])
        self.map[6] = Property(0, properties[2][0], properties[2][1:])
        self.map[8] = Property(0, properties[3][0], properties[3][1:])
        self.map[9] = Property(0, properties[4][0], properties[4][1:])
        self.map[11] = Property(0, properties[5][0], properties[5][1:])
        self.map[13] = Property(0, properties[6][0], properties[6][1:])
        self.map[14] = Property(0, properties[7][0], properties[7][1:])
        self.map[16] = Property(0, properties[8][0], properties[8][1:])
        self.map[18] = Property(0, properties[9][0], properties[9][1:])
        self.map[19] = Property(0, properties[10][0], properties[10][1:])
        self.map[21] = Property(0, properties[11][0], properties[11][1:])
        self.map[23] = Property(0, properties[12][0], properties[12][1:])
        self.map[24] = Property(0, properties[13][0], properties[13][1:])
        self.map[26] = Property(0, properties[14][0], properties[14][1:])
        self.map[27] = Property(0, properties[15][0], properties[15][1:])
        self.map[29] = Property(0, properties[16][0], properties[16][1:])
        self.map[31] = Property(0, properties[17][0], properties[17][1:])
        self.map[32] = Property(0, properties[18][0], properties[18][1:])
        self.map[34] = Property(0, properties[19][0], properties[19][1:])
        self.map[37] = Property(0, properties[20][0], properties[20][1:])
        self.map[39] = Property(0, properties[21][0], properties[21][1:])

        for i in range(4):
            self.map[i * 10 + 5] = Railroad()
        
        self.map[12] = Utility()
        self.map[28] = Utility()