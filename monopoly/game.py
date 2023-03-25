from random import shuffle
from player import Player
from board import Board
from dices import Dices
from property import Property
from railroad import Railroad
from utility import Utility

class Game:
    def __init__(self, players_num: int=2): # the implementation considers only 2 players
        self.players = [Player('Dog'), Player('Car')]

    def action(self, player: Player, board: Board, dices: Dices):
        location = player.move(dices.get_places())
        item = board.get_item_at_location(location)
        if location == 30:
            player.go_to_jail()
        elif isinstance(item, Property):
            if item.get_owner() is None:
                player.buy_or_not(item)
            elif item.get_owner() != player:
                player.pay_rent(item.get_rent())
        elif isinstance(item, Railroad):
            if item.get_owner() is None:
                pass
            elif item.get_owner() != player:
                player.pay_rent(2 ** (item.get_owner().get_number_of_railroads() - 1) * 25)
        elif isinstance(item, Utility):
            if item.get_owner() is None:
                pass
            elif item.get_owner() != player:
                if item.get_owner().get_number_of_utilities() == 1:
                    player.pay_rent(dices.get_places() * 4)
                else: # owner's number of utilities is 2
                    player.pay_rent(dices.get_places() * 10)
        elif isinstance(item, int):
            player.pay_rent(item)

    def turn(self, player: Player, board: Board, dices: Dices) -> None:
        if player.is_in_jail():
            check = input('Give 50$ to get out of jail?[y/n]')
            if check == 'y':
                player.money -= 50
                player.get_out_of_jail()
            elif check == 'n':
                dices.roll()
                if dices.is_double():
                    player.get_out_of_jail()
                elif player.jail_times_increment() > 2:
                    player.money -= 50
                    player.get_out_of_jai()
                else:
                    return
        # --- build buildings or destroy, sell or buy ---
        dices.roll()
        self.action(player, board, dices)
        while dices.is_double():
            if dices.get_double_counter() > 2:
                player.go_to_jail()
            else:
                dices.roll()
                player.move(dices.get_places())
        # for now, we will not prompt the player to end or continue buying, selling,...
        # after moving the token, the turn is over

    def play(self):
        shuffle(self.players)
        limit = 10000
        dices = Dices()
        i = 0
        board = Board()
        for _ in range(limit):
            player = self.players[i]
            self.turn(player, board, dices)
            i = 1 - i

if __name__ == '__main__':
    game = Game()
    game.play()