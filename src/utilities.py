from colorama import Fore
from colorama import Style
import os

def print_with_color(text: str, player) -> None:
    if player.name == 'player1': # this is not a good check!
        print(f'{Fore.BLUE}{text}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}{text}{Style.RESET_ALL}')

properties = [
    # cost, site, rent w/ 1 house, rent w/ 2 houses, rent w/ 3 houses, rent w/ 4 houses, hotel
    ['Mediterranean Avenue', 'brown', 60, 2, 10, 30, 90, 160, 250], # Mediterranean Avenue (brown set)
    ['Baltic Avenue', 'brown', 60, 4, 20, 60, 180, 320, 450], # Baltic Avenue	(brown set)
    ['Oriental Avenue', 'light blue', 100, 6, 30, 90, 270, 400, 550], # Oriental Avenue (light blue set)
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

def railroad_names():
    yield 'Reading Railroad'
    yield 'Pennsylvania Railroad'
    yield 'B. & O. Railroad'
    yield 'Short Line'

sprobabilities = [
    0.030961,
    0.021314,
    0.018849,
    0.021624,
    0.023285,
    0.029631,
    0.022621,
    0.008650,
    0.023210,
    0.023003,
    0.022695, # visiting jail
    0.027017,
    0.026040,
    0.023721,
    0.024649,
    0.029200,
    0.027924,
    0.025945,
    0.029356,
    0.030852,
    0.028836,
    0.028358,
    0.010480,
    0.027357,
    0.031858,
    0.030659,
    0.027072,
    0.026789,
    0.028074,
    0.025861,
    0.000000,
    0.026774,
    0.026252,
    0.023661,
    0.025006,
    0.024326,
    0.008669,
    0.021864,
    0.021799,
    0.026260,
    0.039499 # in jail
]

lprobabilities = [
    0.029143,
    0.020073,
    0.017750,
    0.020369,
    0.021934,
    0.028010,
    0.021317,
    0.008152,
    0.021874,
    0.021680,
    0.021392, # visiting jail
    0.025560,
    0.026140,
    0.021741,
    0.024255,
    0.026354,
    0.026802,
    0.022957,
    0.028210,
    0.028118,
    0.028253,
    0.026143,
    0.010448,
    0.025671,
    0.029929,
    0.028930,
    0.025370,
    0.025191,
    0.026507,
    0.024381,
    0.000000,
    0.025236,
    0.024721,
    0.022276,
    0.023531,
    0.022906,
    0.008158,
    0.020595,
    0.020521,
    0.024832,
    0.094569 # in jail
]

def clear():
    os.system('cls') if os.name == "nt" else os.system('clear')