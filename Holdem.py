﻿
"""
Simulate a round of Holdem with 5 players

"""
#Three objects: Player, Deck, and Hand. Hand is also an attribute of Player
#Player:
class Player:
    #Each player should start off with a set personality type and an amount of money, but the money seems arbitrary, since everyone is going to start off with the same amount of money. Let's define it anyway for the time being. Also, the player starts off with a blank hand.
    def __init__(self,personality,cash):
        self.personality = personality
        self.cash = cash
        self.hand = []
        self.winningHands = []
        
        

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


""" 
#Board: possibly instance of HAND with additional attributes
class Board:
    def __init__(self,cards):
        #Attributes: Pot, Cards on Table, Number of Players, Turn Number
        self.cards = list(cards)
        self.turn = 0
        self.pot = 0
        self.players = 0

    def __str__(self):
        return "The cards on the board are " + str(self.cards)    
#Functions: Assign blinds
"""


"""
TODO
How best to keep hand data for analysis? 
    Options: dict with personality type as key, winning hands as value; 
             dict with round number as key, list of hands as value
             list of lists containing hands for each round 
             SQL database! 
    Needs:
    Frequency of hands given every player stays in through showdown (check accuracy of program with known probabilities)
    Frequency of wins given personality type
    Graph of cash on hand changes throughout game for each personality type
    Statistically significant differences given personality type
establish bet system (bets, pots, cash on hand, blinds) 
develop graphical interface for ease of modifying personality traits and viewing results
develop personality types and alterable traits
"""


from hand import Hand
#create list of players
PlayerList = [
    Player('A',100.00),
    Player('B',100.00),
    Player('C',100.00),
    Player('D',100.00),
    Player('E',100.00)
    ]

winningPlayers = [] #a list of winning players, including their hands

from deck import Deck
deck = Deck()

import sqlite3
handsDb = sqlite3.connect(":memory:")
c = handsDb.cursor()

#create database table
c.execute('''CREATE TABLE hands
            (round integer, player text, hand text, won text, cash real)''')

#start of main program--run simulation a number of times
round = 1
for _ in range(3):

    #shuffle deck, deal two cards to players
    deck.shuffle()

    #deal to players
    for i in PlayerList:
        i.hand = Hand(deck.draw(2))
        

    #deal to the board
    board = Hand(deck.draw(3))

    #board cards are (for practical purposes) added to players hands
    for i in PlayerList:
        i.hand = Hand(i.hand.cards + board.cards)

    #add another card to both the board and the hands
    drawOne = deck.draw(1)
    board.cards = board.cards + drawOne

    for i in PlayerList:
        i.hand = Hand(i.hand.cards + drawOne)

    #draw final card to board
    drawOne = deck.draw(1)

    #add it to both the board and the hands
    board.cards = board.cards + drawOne

    for i in PlayerList:
        i.hand = Hand(i.hand.cards + drawOne)
    
    PlayerList[0].hand.winner = True
    bestHand = PlayerList[0].hand
        
    for i in PlayerList[1:]:
        if i.hand > bestHand:
            bestHand.winner = False
            i.hand.winner = True
        elif i.hand == bestHand:
            i.hand.winner = True

    for i in PlayerList:
        #print(round,i.personality,i.hand,i.hand.winner,i.cash)
        c.execute("INSERT INTO hands VALUES(?,?,?,?,?)",(round,i.personality,str(i.hand),i.hand.winner,i.cash))
    
    handsDb.commit()
    
    
    
    """
    #determine best hand and add winning player to list
    #bestPlayer = [i for i in PlayerList if 
    
    bestHand = PlayerList[0].hand
    #bestPlayer = PlayerList[0]
    
    for i in PlayerList[1:]:
        if i.hand > bestHand:
            bestHand = i.hand
            #bestPlayer = i

    for i in PlayerList:
        if i.hand == bestHand:
            i.winningHands = i.hand
    
    #winningPlayers.append(bestPlayer)
    #for i in winningPlayers:
    #   print (i)
    
    
    #list of players hands for evaluation 
    PlayerHands = []
    for i in PlayerList:
        PlayerHands.append(i.hand)
    
    #lists all winning hand's players for analysis later
    maxValue = max(PlayerHands)

    for i in PlayerList:
        if i.hand == maxValue:
            winningPlayers.append(i)
        #i.hand = []
    """
    round += 1

handsDb.commit()
for row in c.execute('SELECT * FROM hands ORDER BY round'):
        print (row)

    
handsDb.close()

