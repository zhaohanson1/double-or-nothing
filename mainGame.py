import sys
import random
import double_or_nothing_util as dnUtil
import double_or_nothing_game as dnGame
import bot_player as bp
from PyQt5 import QtWidgets, QtGui, QtCore

directoryPath = "playing-cards-assets-master/png/"
backCard = "back.png"
background_path = "background1.jpg"


class dnGameWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.isHumanPlayer = True
        self.botPlayer = bp.BotPlayer()
        self.game = dnGame.DoubleOrNothingGame()
        self.initUI()

    # Initializing Functions
    def initUI(self):
        self.createWindowStyle(background_path)
        self.initButtonsAndLabels()
        self.initBotPlayerInterface()
        self.initSlider()
        self.showMainMenu()
        self.show()

    def createWindowStyle(self, img_path):
        self.setGeometry(100, 100, 600, 300)
        self.setStyleSheet("QPushButton { font: 10pt Arial }")
        bg_img = QtGui.QImage(img_path).scaled(
            QtCore.QSize(600, 300))  # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(bg_img))  # 10 = WindowRole
        self.setPalette(palette)
        self.centerWindow()

    def centerWindow(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def initButtonsAndLabels(self):
        self.initMainMenu()
        self.initTextBox()
        self.initGameButtons()

        self.card1 = QtWidgets.QLabel(self)
        self.card2 = QtWidgets.QLabel(self)

        color = QtGui.QColor(229, 229, 229)
        self.setLabelBgColor(self.card1, color, 255)
        self.setLabelBgColor(self.card2, color, 255)

    def createPushButton(self, name, size, pos, func):
        btn = QtWidgets.QPushButton(name, self)
        btn.resize(size[0], size[1])
        btn.move(pos[0], pos[1])
        btn.clicked.connect(func)
        return btn

    def initMainMenu(self):
        self.computerBtn = self.createPushButton(
            name="Computer",
            size=(100, 100),
            pos=(150, 100),
            func=self.startBotGame)
        self.playBtn = self.createPushButton(
            name="Play",
            size=(100, 100),
            pos=(350, 100),
            func=self.startHumanGame)
        self.menuBtn = self.createPushButton(
            name="Main Menu",
            size=(75, 20),
            pos=(375, 280),
            func=self.showMainMenu)
        self.exitBtn = self.createPushButton(
            name="Exit Game",
            size=(75, 20),
            pos=(525, 280),
            func=self.exitApp)

    def initTextBox(self):
        self.textbox = QtWidgets.QLabel("", self)
        self.textbox.resize(250, 40)
        self.textbox.move(350, 30)
        self.textbox.setStyleSheet(
            "QLabel { font: 9pt Lucida Console; \
                background-color: black; \
                    color: #88d471 }")
        self.textbox.setAlignment(QtCore.Qt.AlignHCenter)
        self.textbox.setFrameStyle(
            QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

    def initGameButtons(self):
        self.higherBtn = self.createPushButton(
            name="Higher",
            size=(75, 75),
            pos=(390, 100),
            func=self.gameChoose)
        self.lowerBtn = self.createPushButton(
            name="Lower",
            size=(75, 75),
            pos=(490, 100),
            func=self.gameChoose)
        self.contBtn = self.createPushButton(
            name="Continue?",
            size=(75, 20),
            pos=(390, 120),
            func=self.gameStep)
        self.restartBtn = self.createPushButton(
            name="Restart",
            size=(75, 20),
            pos=(440, 120),
            func=self.gameRestart)
        self.gameExitBtn = self.createPushButton(
            name="Exit",
            size=(75, 20),
            pos=(440, 150),
            func=self.gameExit)

    def setLabelBgColor(self, label, color, alpha):
        label.setAutoFillBackground(True)
        values = "{r}, {g}, {b}, {a}".format(
            r=color.red(),
            g=color.green(),
            b=color.blue(),
            a=alpha)
        label.setStyleSheet(
            "QLabel { background-color: rgba(" + values + "); }")
        label.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        label.setLineWidth(2)

    def initSlider(self):
        self.sliderLabel = QtWidgets.QLabel('Risk Level', self)
        self.sliderLabel.move(375, 155)
        self.sliderLabelHigh = QtWidgets.QLabel('High', self)
        self.sliderLabelHigh.move(375, 200)
        self.sliderLabelLow = QtWidgets.QLabel('Low', self)
        self.sliderLabelLow.move(550, 200)

        color = QtGui.QColor(255, 255, 255)
        self.setLabelBgColor(self.sliderLabel, color, 255)
        self.setLabelBgColor(self.sliderLabelHigh, color, 255)
        self.setLabelBgColor(self.sliderLabelLow, color, 255)

        self.slider = QtWidgets.QSlider(self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.move(375, 175)
        self.slider.resize(200, 30)
        self.slider.setTickPosition(3)
        self.slider.setValue(50)

        self.slider.valueChanged.connect(self.changeSliderValue)

    def changeSliderValue(self):
        self.game.setRisk(self.slider.value())

    def toggleGameOn(self):
        self.playBtn.hide()
        self.computerBtn.hide()
        self.textbox.show()
        self.menuBtn.show()

    def toggleGameOff(self):
        self.playBtn.show()
        self.computerBtn.show()
        self.textbox.hide()
        self.menuBtn.hide()
        self.higherBtn.hide()
        self.lowerBtn.hide()
        self.contBtn.hide()
        self.restartBtn.hide()
        self.gameExitBtn.hide()
        self.card1.hide()
        self.card2.hide()
        self.valsBox.hide()
        self.initEntry.hide()
        self.nextEntry.hide()

    def showSlider(self):
        self.sliderLabel.show()
        self.sliderLabelHigh.show()
        self.sliderLabelLow.show()
        self.slider.show()

    def hideSlider(self):
        self.sliderLabel.hide()
        self.sliderLabelHigh.hide()
        self.sliderLabelLow.hide()
        self.slider.hide()

    # Menu Functions
    def showMainMenu(self):
        """
        Show menu buttons and hide all non-menu buttons.
        """
        self.game.resetGame()
        self.toggleGameOff()
        self.hideSlider()

    def startHumanGame(self):
        """
        Transition buttons to human game.
        """
        self.isHumanPlayer = True
        self.toggleGameOn()

        self.gameStep()
        self.card1.show()
        self.card2.show()

    def startBotGame(self):
        """
        Transition buttons to bot-assisted game.
        """
        self.isHumanPlayer = False
        self.toggleGameOn()
        self.showSlider()

        self.valsBox.show()
        self.initEntry.show()

        self.setMessage("Enter the first card value.")

    def exitApp(self):
        """
        Exit program. Used for exit button.
        """
        sys.exit()

    def setMessage(self, string):
        """
        Set the text for the textbox.
        """
        self.textbox.setText(string)

    # Game step functions

    def gameStep(self):
        """
        Go to the next step of the game.
        If game started, draw a card from the deck and set it has the
        left card. Otherwise, move the right card to the left.
        """

        deck = self.game.getGameDeck()

        if self.game.getCardTwo() is None:
            newCard = dnUtil.drawCard(deck)
            self.game.setCardOne(newCard)
            self.botPlayer.updateBotCounts(newCard)
        else:
            self.game.setCardOne(self.game.getCardTwo())
            self.game.setCardTwo(None)

        cardOne = self.game.getCardOne()
        cardTwo = self.game.getCardTwo()

        self.updateCardImage(self.card1, cardOne, [20, 20])
        self.updateCardImage(self.card2, backCard, [200, 20])

        if self.isHumanPlayer:
            self.gameStepHuman()
        else:
            self.nextEntry.show()
            self.gameStepBot(cardOne, cardTwo)

    def gameStepHuman(self):
        """
        Human player only needs to update score.
        """
        score = self.game.getScore()
        self.setMessage(
            "Score: " + str(score) +
            ", High Score: " + str(self.game.getHighScore()))
        self.playerPhase()

    def gameStepBot(self, cardOne, cardTwo):
        """
        Bot player needs to update its variables. Also, get the best
        action for current step.
        """
        self.contBtn.hide()
        self.botPlayer.setBase(cardOne)
        self.botPlayer.setUnknownCard(cardTwo)
        state = self.botPlayer.getState()
        bestAction = self.botPlayer.getAction(self.game, state)
        score = self.game.getScore()
        self.setMessage(
            "Score: " + str(score) +
            ", High Score: " + str(self.game.getHighScore()) +
            "\n Best action is " + bestAction.name)

    def updateCardImage(self, label, path, pos):
        """
        Get the card image from file path, then set picture to the LABEL
        at POS
        """
        label.move(pos[0], pos[1])
        pixmap = QtGui.QPixmap(directoryPath + path).scaledToWidth(150)
        label.setPixmap(pixmap)

    def playerPhase(self):
        """
        Player phase is when player predicts if next card is
        higher or lower. Show the action buttons.
        """
        self.higherBtn.show()
        self.lowerBtn.show()
        self.contBtn.hide()
        self.restartBtn.hide()
        self.gameExitBtn.hide()

    def transitionPhase(self, lose=True):
        """
        Player must decide to continue (if possible) or exit.
        """
        self.higherBtn.hide()
        self.lowerBtn.hide()
        if not lose:
            self.contBtn.show()
        self.gameExitBtn.show()

    def gameChoose(self):
        """
        Play the game. User clicks on a choice button.
        We get a draw a card from the deck.
        Compare choice with drawn card and send to next state.
        """
        deck = self.game.getGameDeck()
        cardOne = self.game.getCardOne()
        cardTwo = dnUtil.drawCard(deck)

        self.game.setCardTwo(cardTwo)
        self.updateCardImage(self.card2, cardTwo, [200, 20])
        if not self.isHumanPlayer:
            self.botPlayer.setUnknownCard(cardTwo)
            self.botPlayer.updateBotCounts(cardTwo)
        choice = dnUtil.Action[win.sender().text()]
        self.gameEval(cardOne, cardTwo, choice)

    def gameEval(self, cardOne, cardTwo, choice):
        """
        Check if the player chose the correct action.
        """
        decision = dnUtil.gameDecision(cardOne, cardTwo, choice)
        if decision == 0:
            self.gameTie()
        elif decision == 1:
            self.gameWin()
        elif decision == -1:
            self.gameLose()

    def gameWin(self):
        """
        If you win, update score, ask if exit or continue.
        """
        score = self.game.incrementScore()
        self.setMessage(
            "Score: " + str(score) +
            ", High Score: " + str(self.game.getHighScore()))
        self.gameExitBtn.move(490, 120)
        self.transitionPhase(False)
        if not self.isHumanPlayer:
            self.botDecideExitPhase()

    def gameTie(self):
        """
        If you tie, ask if exit or continue.
        """
        self.gameExitBtn.move(490, 120)
        self.transitionPhase(False)
        if not self.isHumanPlayer:
            self.botDecideExitPhase()

    def gameLose(self):
        """
        If you lose, show score and exit.
        """
        if not self.isHumanPlayer:
            self.botPlayer.setScore(0)
            self.botPlayer.setLoseBool(True)
        self.gameExitBtn.move(440, 120)
        self.transitionPhase(True)

    def botDecideExitPhase(self):
        """
        Bot updates information and chooses post-choice strategy.
        """
        state = self.botPlayer.getState()
        bestAction, winrate = self.botPlayer.getAction(self.game, state)
        score = self.game.getScore()
        self.setMessage(
            "Score: " + str(score) +
            ", High Score: " + str(self.game.getHighScore()) +
            "\n Best action is " + bestAction.name +
            "\n Chance of winning: {:.1f}%".format(winrate))
        if bestAction is dnUtil.Action.Continue:
            self.gameExitBtn.hide()
        else:
            self.contBtn.hide()
        self.nextEntry.hide()

    def gameExit(self):
        """
        End the game, obtain final score.
        """
        self.restartBtn.move(440, 120)
        self.restartBtn.show()
        self.contBtn.hide()
        self.gameExitBtn.hide()

    def gameRestart(self):
        """
        Reset the game and deck.
        """
        if self.isHumanPlayer:
            self.restartBtn.hide()
            score = self.game.resetScore()
            self.setMessage(
                "Score: " + str(score) +
                ", High Score: " + str(self.game.getHighScore()))
            self.game.resetDeck()
            self.game.setCardTwo(None)
            self.gameStep()
        else:
            self.botPlayer.resetBot()
            self.showMainMenu()
            self.startBotGame()

    # Bot related functions
    def initBotPlayerInterface(self):
        """
        Setup drop-down menus for values and suits.
        """
        self.valsBox = QtWidgets.QComboBox(self)
        self.valsBox.setObjectName(("Values"))
        for value in dnUtil.valuesList:
            self.valsBox.addItem(value.upper())
        self.valsBox.resize(75, 20)
        self.valsBox.move(375, 100)

        self.initEntry = self.createPushButton(
            name='Display card',
            size=(85, 30),
            pos=(435, 220),
            func=self.initBot)
        self.nextEntry = self.createPushButton(
            name='Display card',
            size=(85, 30),
            pos=(435, 220),
            func=self.botStep)

    def getCardFromInput(self):
        inputValue = str(self.valsBox.currentText()).lower()
        randomSuit = dnUtil.suitsList[random.randint(0, 3)]
        return dnUtil.getCardString(inputValue, randomSuit)

    def initBot(self):
        """
        Get information from input to set first card.
        """
        self.initEntry.hide()
        card = self.getCardFromInput()
        self.game.setCardOne(card)
        self.botPlayer.setBase(card)
        self.botPlayer.setUnknownCard(None)
        self.botPlayer.updateBotCounts(card)
        self.updateCardImage(self.card1, card, [20, 20])
        self.updateCardImage(self.card2, backCard, [200, 20])

        state = self.botPlayer.getState()
        bestAction = self.botPlayer.getAction(self.game, state)
        score = self.game.getScore()
        self.setMessage(
            "Score: " + str(score) +
            ", High Score: " + str(self.game.getHighScore()) +
            "\n Best action is " + bestAction.name +
            "\n Select the card that displayed")
        self.nextEntry.show()
        self.card1.show()
        self.card2.show()

    def botStep(self):
        """
        Display the card entered in the input text fields.
        Give the best action for the current state.
        """
        card = self.getCardFromInput()
        self.game.setCardTwo(card)
        self.botPlayer.setUnknownCard(card)
        self.botPlayer.updateBotCounts(card)
        self.updateCardImage(self.card2, card, [200, 20])

        base = self.game.getCardOne()
        baseVal = dnUtil.getValue(base)
        otherVal = dnUtil.getValue(card)
        if dnUtil.compareValue(baseVal, otherVal) > 0:
            self.gameEval(base, card, dnUtil.Action.Lower)
        else:
            self.gameEval(base, card, dnUtil.Action.Higher)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = dnGameWindow()
    sys.exit(app.exec_())
