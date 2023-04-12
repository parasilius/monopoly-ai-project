from utility import Utility
from property import Property
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
    
    def get_build_score(self, player, other_player, depth, bestScore, node):
        for prop in player.get_buildable_properties():
            player_copy = copy.deepcopy(player)
            cost = prop.build_house()
            player_copy.lose_money(cost)
            player_copy.net_worth += cost / 2.0
            score = self.get_heuristic(player_copy, other_player, node, depth)
            prop.destroy_house()
            if node == 'expMin':
                bestScore = max(score, bestScore)
            else:
                bestScore = min(score, bestScore)
        return bestScore
    
    def get_destroy_score(self, player, other_player, depth, bestScore, node):
        for prop in player.get_destroyable_properties():
            player_copy = copy.deepcopy(player)
            cash = prop.destroy_house()
            player_copy.gain_money(cash)
            player_copy.net_worth -= cash * 2
            score = self.get_heuristic(player_copy, other_player, node, depth)
            prop.build_house()
            if node == 'expMin':
                bestScore = max(score, bestScore)
            else:
                bestScore = min(score, bestScore)
        return bestScore
    
    def get_upgrade_score(self, player, other_player, depth, bestScore, node):
        for prop in player.get_buildable_properties():
            if prop.get_number_of_houses() == 4:
                player_copy = copy.deepcopy(player)
                cost = prop.upgrade_houses_to_hotel()
                player_copy.lose_money(cost)
                player_copy.net_worth += 2 * cost
                score = self.get_heuristic(player_copy, other_player, node, depth)
                prop.downgrade_hotel_to_houses()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        return bestScore
    
    def get_downgrade_score(self, player, other_player, depth, bestScore, node):
        for prop in player.get_downgradable_properties():
            player_copy = copy.deepcopy(player)
            cost = prop.downgrade_hotel_to_houses()
            player_copy.lose_money(cost)
            self.net_worth += 8 * cost
            score = self.get_heuristic(player_copy, other_player, node, depth)
            prop.upgrade_houses_to_hotel()
            if node == 'expMin':
                bestScore = max(score, bestScore)
            else:
                bestScore = min(score, bestScore)
        return bestScore
    
    def get_unmortgage_score(self, player, other_player, depth, bestScore, node):
        for prop in player.get_properties():
            if not prop.is_mortgaged and prop.number_of_houses == 0 and prop.number_of_hotels == 0:
                player_copy = copy.deepcopy(player)
                player_copy.gain_money(prop.mortgage())
                score = self.get_heuristic(player_copy, other_player, node, depth)
                prop.unmortgage()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        for railroad in player.railroads:
            if not railroad.is_mortgaged:
                player_copy = copy.deepcopy(player)
                player_copy.gain_money(railroad.mortgage())
                score = self.get_heuristic(player_copy, other_player, node, depth)
                railroad.unmortgage()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        for util in player.utilities:
            if not util.is_mortgaged:
                player_copy = copy.deepcopy(player)
                player_copy.gain_money(util.mortgage())
                score = self.get_heuristic(player_copy, other_player, node, depth)
                util.unmortgage()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        return bestScore

    def get_mortgage_score(self, player, other_player, depth, bestScore, node):
        for prop in player.get_properties():
            if prop.is_mortgaged:
                player_copy = copy.deepcopy(player)
                player_copy.lose_money(prop.unmortgage())
                score = self.get_heuristic(player_copy, other_player, node, depth)
                prop.mortgage()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        for railroad in player.railroads:
            if railroad.is_mortgaged:
                player_copy = copy.deepcopy(player)
                player_copy.lose_money(railroad.unmortgage())
                score = self.get_heuristic(player_copy, other_player, node, depth)
                railroad.mortgage()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        for util in player.utilities:
            if util.is_mortgaged:
                player_copy = copy.deepcopy(player)
                player_copy.lose_money(util.unmortgage())
                score = self.get_heuristic(player_copy, other_player, node, depth)
                util.mortgage()
                if node == 'expMin':
                    bestScore = max(score, bestScore)
                else:
                    bestScore = min(score, bestScore)
        return bestScore
    
    def get_score_generate(self):
        yield self.get_build_score
        yield self.get_destroy_score
        yield self.get_upgrade_score
        yield self.get_downgrade_score
        yield self.get_unmortgage_score
        yield self.get_mortgage_score

    def get_heuristic(self, player, other_player, node, depth=4):
        if depth == 0 or player.is_bankrupt() or other_player.is_bankrupt() or player.is_in_jail():
            return self.heuristic(player, other_player)
        if node == 'max':
            bestScore = float('-inf')
            for get_score_function in self.get_score_generate():
                bestScore = get_score_function(player, other_player, depth - 1, bestScore, 'expMin')
            if bestScore == float('-inf'):
                return 0
            return bestScore
        elif node == 'min':
            bestScore = float('inf')
            for get_score_function in self.get_score_generate():
                bestScore = get_score_function(other_player, player, depth - 1, bestScore, 'expMax')
            if bestScore == float('inf'):
                return 0
            return bestScore
        elif node == 'expMax':
            bestScore = 0
            for i in range(1, 7):
                for j in range(1, 7):
                    player_copy = copy.deepcopy(player)
                    player_copy.lose_money(50)
                    player_copy.location += i + j
                    bestScore += (1 / 36.0) * self.get_heuristic(player_copy, other_player, 'max', depth - 1)
                    player_copy.location -= i + j
            return bestScore
        elif node == 'expMin':
            bestScore = 0
            for i in range(1, 7):
                for j in range(1, 7):
                    player_copy = copy.deepcopy(player)
                    player_copy.lose_money(50)
                    player_copy.location += i + j
                    bestScore += (1 / 36.0) * self.get_heuristic(player_copy, other_player, 'min', depth - 1)
                    player_copy.location -= i + j
            return bestScore

    def decide(self, player, other_player, board, dice):
        bestScore = float('-inf')
        best_buy = None
        move = None
        best_location = None
        for buy in [True, False]:
            board_copy = copy.deepcopy(board)
            first_copy = copy.deepcopy(player)
            first_copy.action(board_copy, dice, buy)
            player_copy = copy.deepcopy(first_copy)
            score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
            if bestScore <= score:
                bestScore = score
                best_buy = buy
            for prop in first_copy.get_buildable_properties():
                player_copy = copy.deepcopy(first_copy)
                cost = prop.build_house()
                player_copy.lose_money(cost)
                player_copy.net_worth += cost / 2.0
                score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                prop.destroy_house()
                if bestScore <= score:
                    bestScore = score
                    move = 0
                    best_location = prop.location
                    best_buy = buy
            for prop in first_copy.get_destroyable_properties():
                player_copy = copy.deepcopy(first_copy)
                cash = prop.destroy_house()
                player_copy.gain_money(cash)
                player_copy.net_worth -= cash * 2
                score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                prop.build_house()
                if bestScore <= score:
                    bestScore = score
                    move = 1
                    best_location = prop.location
                    best_buy = buy
            for prop in first_copy.get_buildable_properties():
                if prop.get_number_of_houses() == 4:
                    player_copy = copy.deepcopy(first_copy)
                    cost = prop.upgrade_houses_to_hotel()
                    player_copy.lose_money(cost)
                    player_copy.net_worth += 2 * cost
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    prop.downgrade_hotel_to_houses()
                    if bestScore <= score:
                        bestScore = score
                        move = 2
                        best_location = prop.location
                        best_buy = buy
            for prop in first_copy.get_downgradable_properties():
                player_copy = copy.deepcopy(first_copy)
                cost = prop.downgrade_hotel_to_houses()
                player_copy.lose_money(cost)
                self.net_worth += 8 * cost
                score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                prop.upgrade_houses_to_hotel()
                if bestScore <= score:
                    bestScore = score
                    move = 3
                    best_location = prop.location
                    best_buy = buy
            for prop in first_copy.get_properties():
                if not prop.is_mortgaged and prop.number_of_houses == 0 and prop.number_of_hotels == 0:
                    player_copy = copy.deepcopy(first_copy)
                    player_copy.gain_money(prop.mortgage())
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    prop.unmortgage()
                    if bestScore <= score:
                        bestScore = score
                        move = 4
                        best_location = prop.location
                        best_buy = buy
            for railroad in first_copy.railroads:
                if not railroad.is_mortgaged:
                    player_copy = copy.deepcopy(first_copy)
                    player_copy.gain_money(railroad.mortgage())
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    railroad.unmortgage()
                    if bestScore <= score:
                        bestScore = score
                        move = 4
                        best_location = railroad.location
                        best_buy = buy
            for util in first_copy.utilities:
                if not util.is_mortgaged:
                    player_copy = copy.deepcopy(first_copy)
                    player_copy.gain_money(util.mortgage())
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    util.unmortgage()
                    if bestScore <= score:
                        bestScore = score
                        move = 4
                        best_location = util.location
                        best_buy = buy
            for prop in first_copy.get_properties():
                if prop.is_mortgaged:
                    player_copy = copy.deepcopy(first_copy)
                    player_copy.lose_money(prop.unmortgage())
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    prop.mortgage()
                    if bestScore <= score:
                        bestScore = score
                        move = 5
                        best_location = prop.location
                        best_buy = buy
            for railroad in first_copy.railroads:
                if railroad.is_mortgaged:
                    player_copy = copy.deepcopy(first_copy)
                    player_copy.lose_money(railroad.unmortgage())
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    railroad.mortgage()
                    if bestScore <= score:
                        bestScore = score
                        move = 5
                        best_location = railroad.location
                        best_buy = buy
            for util in first_copy.utilities:
                if util.is_mortgaged:
                    player_copy = copy.deepcopy(first_copy)
                    player_copy.lose_money(util.unmortgage())
                    score = player_copy.strategy.get_heuristic(player_copy, other_player, 'max')
                    util.mortgage()
                    if bestScore <= score:
                        bestScore = score
                        move = 5
                        best_location = util.location
                        best_buy = buy
        return best_buy, move, best_location