from colorama import Fore
from colorama import Style

def print_with_color(text: str, player) -> None:
    if player.player_name == 'player_bot': # this is not a good check!
        print(f'{Fore.BLUE}{text}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}{text}{Style.RESET_ALL}')