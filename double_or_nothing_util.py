import random
import itertools

valuesList = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
              "jack", "queen", "king", "ace"]
suitsList = ["clubs", "diamonds", "hearts", "spades"]


class DoubleOrNothingGame:

    def __init__(self, deck):
        self.randCard = None
        self.randCard2 = None
        self.deck = deck
        self.score = 1
        self.highScore = 0
        self.risk = 50

    def setRisk(self, risk):
        self.risk = risk

    def getRisk(self):
        return self.risk

    def resetGame(self):
        self.__init__(getDeck())

    def getGameState(self):
        return (self.randCard, self.randCard2, self.deck)

    def getScore(self):
        return self.score

    def getHighScore(self):
        return self.highScore

    def incrementScore(self):
        self.score *= 2
        if self.score > self.highScore:
            self.highScore = self.score
        return self.score

    def resetScore(self):
        self.score = 1
        return self.score

    def resetDeck(self):
        self.deck = getDeck()

    def getGameDeck(self):
        return self.deck

    def setRandCard(self, card):
        self.randCard = card

    def setRandCard2(self, card):
        self.randCard2 = card

    def getRandCard(self):
        return self.randCard

    def getRandCard2(self):
        return self.randCard2


def getDeck():
    deck = itertools.product(valuesList, suitsList)
    deck = list(deck)
    random.shuffle(deck)
    return deck


def drawCard(deck):
    if deck is None:
        print("Perfect game acheived")
        return None
    cardPair = deck.pop()
    return getCardString(cardPair[0], cardPair[1])


def getCardString(value, suit):
    if value == "joker":
        return suit + "_" + value + ".png"
    return value + "_of_" + suit + ".png"


def dummyCard(value):
    return getCardString(value, "clubs")


def getValue(path):
    """
    Returns the value of a card.
    """
    splitPath = path.split('_')
    if splitPath[1] == "joker.png":
        return "joker"
    return splitPath[0]


def getRandomCard(joker=False):
    jokerProb = 0.037
    colorProb = 0.5
    if joker and random.random() < jokerProb:
        if random.random() < colorProb:
            return getCardString("joker", "red")
        else:
            return getCardString("joker", "black")
    vals = random.randint(0, len(valuesList) - 1)
    suit = random.randint(0, len(suitsList) - 1)
    return getCardString(valuesList[vals], suitsList[suit])


def compareValue(value1, value2):
    comp1 = valuesList.index(value1)
    comp2 = valuesList.index(value2)
    return comp1 - comp2


def gameDecision(card1, card2, choice):
    """
    Evaluates the game for the given choice. 
    Return 1 if it's a win, 0 if tie, and -1 if loss
    """
    value1 = getValue(card1)
    value2 = getValue(card2)
    comp = compareValue(value1, value2)
    if comp == 0:
        return 0
    elif comp < 0:
        return 1 if choice == "Higher" else -1
    else:
        return 1 if choice == "Lower" else -1
