import double_or_nothing_util as dnUtil
import sys
import math


class BotPlayer:

    def __init__(self):
        self.state = [None, None, None, False]
        self.score = 0
        counts = {}
        for value in dnUtil.valuesList:
            counts[value] = calcDefaultCount(value)
        self.state[2] = counts

    def resetBot(self):
        self.__init__()

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def getBase(self, state):
        return state[0]

    def setBase(self, card):
        self.state[0] = dnUtil.getValue(card)

    def getUnknown(self, state):
        return state[1]

    def setUnknown(self, card):
        if card is not None:
            self.state[1] = dnUtil.getValue(card)
        else:
            self.state[1] = None

    def getCounts(self, state):
        return state[2]

    def setCounts(self, counts):
        self.state[2] = counts

    def setLoseBool(self, lose):
        self.state[3] = lose

    def getLoseBool(self, state):
        return state[3]

    def expectancyPcnt(self, p):
        """
        Simplified trade expectancy formula.
        """
        return (2 * p) - 1

    def getAction(self, game, state):
        if self.getUnknown(state) is None:
            possibleAct = ["Higher", "Lower"]
            baseVal = self.getBase(state)
            counts = self.getCounts(state)[baseVal]
            if counts[0] > counts[1]:
                return "Higher"
            elif counts[0] < counts[1]:
                return "Lower"
            else:
                return "Higher" if dnUtil.random.random() > 50 else "Lower"
        elif self.getLoseBool(state):
            return "Exit"
        else:
            nextVal = self.getUnknown(state)
            nextCounts = self.getCounts(state)[nextVal]
            deckSize = sum(nextCounts)
            high, low, tie = nextCounts

            if high > low:
                winrate = high / deckSize
            elif high < low:
                winrate = low / deckSize
            else:
                winrate = 0.5

            print(winrate)
            risk = game.getRisk()
            if self.expectancyPcnt(winrate) > self.expectancyPcnt(risk / 100):
                return "Continue?"
            else:
                return "Exit"

    def updateBotCounts(self, drawCard):
        nextVal = dnUtil.getValue(drawCard)
        state = self.getState()
        counts = self.getCounts(state)
        newCount = counts.copy()
        for value in dnUtil.valuesList:
            if counts[value][2] == 0:
                continue
            update = updateCount(value, nextVal, counts[value])
            newCount[value] = update
        self.setCounts(newCount)


def calcDefaultCount(value):
    idx = dnUtil.valuesList.index(value)
    higher = (len(dnUtil.valuesList) - idx - 1) * 4
    lower = idx * 4
    tie = 4
    return (higher, lower, tie)


def updateCount(cardVal, nextVal, counts):
    higher, lower, tie = counts
    comp = dnUtil.compareValue(cardVal, nextVal)
    if comp == 0:
        tie -= 1
    elif comp < 0:
        higher -= 1
    else:
        lower -= 1
    return (higher, lower, tie)
