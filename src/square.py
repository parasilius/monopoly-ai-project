class Square:
    '''
    lprobability: Long Term Probability for Ending Up on the Square(Jail Long)
    sprobability: Short Term Probability for Ending Up on the Square(Jail Short)
    '''
    def __init__(self, cost: int, lprobability: float, sprobability: float):
        self.cost = cost
        self.lprobability = lprobability
        self.sprobability = sprobability