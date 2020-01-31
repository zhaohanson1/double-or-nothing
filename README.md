Double or Nothing
=======

Problem Formulation: You are playing a double or nothing game with a deck of cards without replacement. You initially draw the top card of the deck. 
On the first turn, you guess whether the next card will be higher or lower.
Your reward for guessing correctly is 1 point and on the subsequent turns, you double your money. 
However, if you lose, you will lose all of the money you have earned.
After the reward, you can decide whether to continue the game or exit with your money. If you continue, the last card you drew will be the card for the next round.

### Solving higher or lower
Keep track of how many cards are higher/lower/tied with every value. Then, simply choose which value is the highest for the current value. Ties will not effect our score, so they do not have to be taken into account.

### Solving continuing or exiting
Check the probability of winning for the next card. We know we will always choose optimally, so the action is always set. We use a expectancy formula to calculate our expected winnings, which indicates how much you are expected to win per unit.

### Risk factor
Since we may want to have higher risk towards the beginning since we do not lose much and lower risk towards the end as we do not want to lose a larger amount, the threshold of expectancy is changeable by the slider.

### How to Play
Select `Computer` to start the game helper. This is to be used in tandem with a randomized game.

Select `Play` to start a human controlled game. 

## Play
The game will display a card, and the player must guess whether the next card will be higher or lower. On a correct choice, the player's score will double. On an incorrect choice, the player will lose all their points and the game will exit. 

After a win, the player can choose to continue playing, or exit with their score. The highest score will be recorded.

## Computer
First, the user must choose the intial value. Then, the program will display the most likely choice of winning. The player will choose this in the game they are playing and must enter the value of the next card. The program will then display whether the user should continue or exit. The risk factor can be changed before entering the next value to influence the continue/exit decision.

-------
Run the program using the `mainGame.py`file.
