import double_or_nothing_util as dnUtil
import sys
import math


class BotPlayer:

    def __init__(self):
        self.resetBot()

    def resetBot(self):
        self.state = [None, None, None, False]
        self.score = 0
        counts = {}
        for value in dnUtil.valuesList:
            counts[value] = calcDefaultCount(value)
        self.state[2] = counts

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

    def getUnknownCard(self, state):
        return state[1]

    def setUnknownCard(self, card):
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
        if self.getUnknownCard(state) is None:
            baseVal = self.getBase(state)
            counts = self.getCounts(state)[baseVal]
            if counts[0] > counts[1]:
                return dnUtil.Action.Higher
            elif counts[0] < counts[1]:
                return dnUtil.Action.Lower
            else:
                if dnUtil.random.random() > 50:
                    return dnUtil.Action.Higher
                else:
                    return dnUtil.Action.Lower
        elif self.getLoseBool(state):
            return dnUtil.Action.Exit
        else:
            nextVal = self.getUnknownCard(state)
            nextCounts = self.getCounts(state)[nextVal]
            deckSize = sum(nextCounts)
            high, low, tie = nextCounts

            if high > low:
                winrate = high / deckSize
            elif high < low:
                winrate = low / deckSize
            else:
                winrate = 0.5

            risk = game.getRisk()
            if self.expectancyPcnt(winrate) > self.expectancyPcnt(risk / 100):
                return dnUtil.Action.Continue, winrate * 100
            else:
                return dnUtil.Action.Exit, winrate * 100

    def updateBotCounts(self, nextCard):
        nextVal = dnUtil.getValue(nextCard)
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
