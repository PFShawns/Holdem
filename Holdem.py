﻿#import deck
#import hand

"""
Simulate a round of Holdem with 5 players

"""
#Three objects: Player, Deck, and Table 
#Player:
class Player:
    #Each player should start off with a set personality type and an amount of money, but the money seems arbitrary, since everyone is going to start off with the same amount of money. Let's define it anyway for the time being. Also, the player starts off with a blank hand.
    def __init__(self,personality,cash,hand):
        self.personality = personality
        self.cash = cash
        self.hand = hand
        

    #a method to print the object normally as a string for debugging or whatever
    def __str__(self):
        return "Personality type " + str(self.personality) + " with " + str(self.cash) + " dollars holding " + str(self.hand)
        

    #Methods: Evaluate, Bet

    #Evaluate--takes players hand, cards shown on the board, and returns list of potential hands and probability of getting an out using the 4-2 rule
    #Better than checking each possible hand is probably to check for each type of hand, starting with straight flush, four of a kind, etc.
    
    def evaluate(self,board):

        #make a combined list of cards to include board and hand
        self.cardSet = self.hand + board.cards

        #which turn it is determines the means:

        #turn 1 has no board cards, so the evaluation can be a basic strength ranking
        #https://commons.wikimedia.org/wiki/File:Sklansky-Malmuth_Texas_Holdem_Starting_Hand_Strategy.JPG
        

        #turn 2 -- number of outs times 4 
        #turn 3 -- number of outs times 2
        

        
        



    #BetResponse--takes evaluation and check, calls, raises, or folds based on personality, pot size, bet amount, and the limitation of cash on hand
    def betResponse(self,bet,pot):
        self.check = False
        self.call = False
        self._raise = False
        self.fold = False

    #establish bet threshhold based on personality and evaluation (scale 0-4)
        #Type A -- equal to evaluation
        #Type B -- equal to evaluation
        #Type C -- evaluation x 1.5
        #Type D -- evaluation x 1.5
        #Type E -- evaluation x 2

    #determine bet level based on pot size and bet amount (scale 0-4)
        #no bet -- 0 points
        #minimum bet -- 1 point
        #bet half pot -- 2 points
        #bet pot -- 3 points
        #all in (if greater than 2x pot) -- 4 points

    #if threshhold under bet level, check or fold
        
    #if threshhold over or equal, call, check, or raise        

#Deck:

#Functions: Shuffle, Deal -- three types of deal based on stage of game
#Properties: Count -- number of cards remaining in deck
#Board:
class Board:
    def __init__(self,cards):
        #Attributes: Pot, Cards on Table, Number of Players, Turn Number
        self.cards = cards
        self.turn = 0
        self.pot = 0
        self.players = 0

    def __str__(self):
        return "The cards on the board are " + str(self.cards)    
#Functions: Assign blinds




#Debugging

#deal two cards to players, assign personalities and provide cash
from deck import Deck
pile = Deck()

from hand import Hand
first = Hand(pile.draw(2)) 
second = Hand(pile.draw(2))

firstPlayer = Player('A',100.00,first)
secondPlayer = Player('B',100.00,second)

dealToBoard = Hand(pile.draw(3))
b = Board(dealToBoard)

#board cards are (for practical purposes) added to players hand
"""alternatively and probably better to print out as a string but keep objects separate
maybe by passing board to player method evaluate
"""
firstPlayer.hand = Hand(firstPlayer.hand.cards + b.cards.cards)
secondPlayer.hand = Hand(secondPlayer.hand.cards + b.cards.cards)

#draw another card to the board
b.cards2 = Hand(pile.draw(1))

#add to players hand
firstPlayer.hand = Hand(firstPlayer.hand.cards + b.cards2.cards)
secondPlayer.hand = Hand(secondPlayer.hand.cards + b.cards2.cards)

#draw final card to board
b.cards3 = Hand(pile.draw(1))

#add to players hand
firstPlayer.hand = Hand(firstPlayer.hand.cards + b.cards3.cards)
secondPlayer.hand = Hand(secondPlayer.hand.cards + b.cards3.cards)

""" can we combine hand and cards? """

"""TODO -- compare hands"""


print (firstPlayer)
print (secondPlayer)


