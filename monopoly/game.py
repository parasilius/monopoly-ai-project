from random import shuffle
from player import Player
from board import Board
from dice import Dice
from property import Property
from railroad import Railroad
from utility import Utility

class Game:
    def __init__(self, players_num: int=2): # the implementation considers only 2 players
        self.players = [Player('Human'), Player('AI')]

    def action(self, player: Player, board: Board, dice: Dice):
        location = player.move(dice.get_places())
        item = board.get_item_at_location(location)
        if location == 30:
            player.go_to_jail()
        elif isinstance(item, Property):
            if item.get_owner() is None:
                player.buy_or_not(item)
            elif item.get_owner() != player:
                player.pay_rent(item.get_rent(), item.get_owner())
        elif isinstance(item, Railroad):
            if item.get_owner() is None:
                pass
            elif item.get_owner() != player:
                player.pay_rent(2 ** (item.get_owner().get_number_of_railroads() - 1) * 25, item.get_owner())
        elif isinstance(item, Utility):
            if item.get_owner() is None:
                pass
            elif item.get_owner() != player:
                if item.get_owner().get_number_of_utilities() == 1:
                    player.pay_rent(dice.get_places() * 4, item.get_owner())
                else: # owner's number of utilities is 2
                    player.pay_rent(dice.get_places() * 10, item.get_owner())
        elif isinstance(item, int):
            player.pay_rent(item)

    def turn(self, player: Player, board: Board, dice: Dice) -> None:
        player.build_or_not()
        if player.is_in_jail():
            check = input('Give 50$ to get out of jail?[y/n] ')
            if check == 'y':
                player.lose_money(50)
                player.get_out_of_jail()
            elif check == 'n':
                dice.roll(player)
                if dice.is_double():
                    player.get_out_of_jail()
                elif player.jail_times_increment() > 2:
                    player.lose_money(50)
                    player.get_out_of_jail()
                else:
                    return
        # --- build buildings or destroy, sell or buy ---
        global available_houses
        global available_hotels
        dice.roll(player)
        self.action(player, board, dice)
        double_counter = 0
        while dice.is_double():
            double_counter += 1
            if double_counter > 2:
                player.go_to_jail()
                return
            else:
                dice.roll(player)
                player.move(dice.get_places())
        # for now, we will not prompt the player to end or continue buying, selling,...
        # after moving the token, the turn is over

    def check_winning(self) -> Player:
        for i in range(1):
            if self.players[i].get_money() == 0:
                return self.players[1 - 1]
        return None

    def play(self):
        shuffle(self.players)
        limit = 10000
        dice = Dice()
        i = 0
        board = Board()
        for _ in range(limit):
            player = self.players[i]
            if self.check_winning() == None:
                self.turn(player, board, dice)
                i = 1 - i
            else:
                print(f'player {self.check_winning()} wins.')
                break

if __name__ == '__main__':
    game = Game()
    game.play()