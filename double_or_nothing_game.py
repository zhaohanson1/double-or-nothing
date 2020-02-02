import double_or_nothing_util as dnUtil


class DoubleOrNothingGame:

    def __init__(self):
        self.resetGame()

    def resetGame(self):
        self.cardOne = None
        self.cardTwo = None
        self.deck = dnUtil.getNewDeck()
        self.score = 1
        self.highScore = 0
        self.risk = 50

    def incrementScore(self):
        self.score *= 2
        if self.score > self.highScore:
            self.highScore = self.score
        return self.score

    def resetScore(self):
        self.score = 1
        return self.score

    def resetDeck(self):
        self.deck = dnUtil.getNewDeck()

    def getCardOne(self):
        return self.cardOne

    def setCardOne(self, card):
        self.cardOne = card

    def getCardTwo(self):
        return self.cardTwo

    def setCardTwo(self, card):
        self.cardTwo = card

    def getGameDeck(self):
        return self.deck

    def getGameState(self):
        return (self.cardOne, self.cardTwo, self.deck)

    def getHighScore(self):
        return self.highScore

    def getRisk(self):
        return self.risk

    def setRisk(self, risk):
        self.risk = risk

    def getScore(self):
        return self.score
