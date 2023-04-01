from first_agent import FirstAgent
from utility import Utility

class SecondAgent(FirstAgent):
    def buy_or_not(self, item):
        if isinstance(item, Utility):
            return -1
        return self.buy(item)