from utility import Utility
import copy

class Strategy:
    def __init__(self, reserve, reserve_penalty, rent_mp, opponent_rent_mp):
        self.reserve = reserve
        self.reserve_penalty = reserve_penalty
        self.rent_mp = rent_mp
        self.opponent_rent_mp = opponent_rent_mp

    def evaluate_jail_stay(self, player, other_player, board, stay_in_jail: bool) -> float:
        if player.is_bankrupt():
            return float('-inf')
        if stay_in_jail:
            return 0
        elif board.map[player.location] != None and not isinstance(board.map[player.location], int):
            if board.map[player.location].owner != None and board.map[player.location].owner.name == other_player.name and not board.map[player.location].is_mortgaged:
                if isinstance(board.map[player.location], Utility):
                    player.pay_rent(board.map[player.location].get_rent(2)) # no need for other arguments
                else:
                    player.pay_rent(board.map[player.location].get_rent()) # no need for other arguments
                if player.is_bankrupt():
                    return float('-inf')
                return -1
            elif board.map[player.location].owner == None:
                player.buy(board.map[player.location]) # buying is better than not buying in the first turns
                if player.is_bankrupt():
                    return float('-inf')
                if isinstance(board.map[player.location], Utility):
                    return 0
                return 1
        return 0

    def get_jail_heuristic(self, player, other_player, depth: int, board, stay_in_jail: bool) -> float:
        if stay_in_jail or depth == 0 or player.is_bankrupt() or other_player.is_bankrupt():
            return self.evaluate_jail_stay(player, other_player, board, stay_in_jail)
        else:
            bestScore = 0
            for i in range(1, 7):
                for j in range(1, 7):
                    player_copy = copy.deepcopy(player)
                    player_copy.lose_money(50)
                    player_copy.location += i + j
                    bestScore += (1 / 36.0) * self.get_jail_heuristic(player_copy, other_player, depth - 1, board, False)
                    player_copy.location -= i + j
            return bestScore

    def heuristic(self, player, other_player):
        score = player.net_worth - other_player.net_worth
        for prop in player.get_properties():
            score += self.rent_mp * prop.get_rent()
        
        for prop in other_player.get_properties():
            score -= self.opponent_rent_mp * prop.get_rent()

        if player.money < self.reserve:
            score -= self.reserve_penalty

        return score