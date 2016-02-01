
"""
Simulate a round of Holdem with 5 players


"""

#Player:
class Player:
    #Each player should start off with a set personality type and an amount of money, but the money seems arbitrary, since everyone is going to start off with the same amount of money. Let's define it anyway for the time being. Also, the player starts off with a blank hand.
    def __init__(self,personality,cash):
        self.personality = personality
        self.cash = cash
        self.hand = []
        self.winningHands = []
        self.betAmount = 0
        self.fold = False
        self.outOfGame = False
        
        

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
    """
    def betResponse(self,bet,pot):
        self.check = False
        self.call = False
        self._raise = False
        self.fold = False
    """
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


 
#Board: possibly instance of HAND with additional attributes
class Board:
    def __init__(self,iterator):
        #Attributes: Pot, Cards on Table, Number of Players, Turn Number
        #self.playerList = playerList
        #self.cards = []
        #self.turn = 0
        self.pot = 0
        self.iterator = iterator
        self.ties = 0
        #self.players = 0

    def __str__(self):
        return "The cards on the board are " + str(self.cards)   
    
    def placeBlinds(self):        

        #place little blind
        next(self.iterator).cash -= 5
        #placeHolder.betAmount = 5
  
        #place big blind
        next(self.iterator).cash -= 10
        #placeHolder.betAmount = 

        #move the iterator back to the little blind and assign a bet amount
        next(self.iterator)
        next(self.iterator)
        next(self.iterator)
        next(self.iterator).betAmount += 5

        #assign the bet amount to the big blind
        next(self.iterator).betAmount += 10

        #move the iterator back to the big blind for the next round
        next(self.iterator)
        next(self.iterator)
        next(self.iterator)
        next(self.iterator)





"""
TODO
    
Graph of cash on hand changes throughout game for each personality type
Establish bet system (bets, pots, cash on hand, blinds) 
Develop graphical interface for ease of modifying personality traits and viewing results
Develop personality types and alterable traits

BUGS

check: accuracy of tie count and hands


"""


from hand import Hand
#create list of players
PlayerList = [
    Player('A',1000.00),
    Player('B',1000.00),
    Player('C',1000.00),
    Player('D',1000.00),
    Player('E',1000.00)
    ]

from deck import Deck

import sqlite3
handsDb = sqlite3.connect(":memory:")
c = handsDb.cursor()

#create database table
c.execute('''CREATE TABLE hands
            (round integer, player text, hand text, cards text, value integer, won text, cash real)''')

import random
#start of main program--run simulation a number of times put results in database
round = 1

import itertools

button = itertools.cycle(PlayerList)

boardFunc = Board(button)



#number of hands to run through -- 1000 seems like a sufficient amount for initial runs
for _ in range(1000):

    boardFunc.pot = 0

    boardFunc.placeBlinds()        
          
    #shuffle deck, deal two cards to players
    #new deck
    deck = Deck()
    random.shuffle(deck.remaining)
    
    #deal to players
    for i in PlayerList:
        if i.cash >= 10:
            #everyone back in the game that folded last hand, unless they are out of the game
            i.fold = False
            i.hand = Hand(deck.draw(2))
        else:
            i.fold = True
        
    
    
    #each player in turn evaluates whether to stay in, placing a minimum bet equal to the big blind

    

    #determine the highest bet amount
    betsPlaced = []
    for i in PlayerList:
        betsPlaced.append(i.betAmount)

    highestBet = max(betsPlaced)

    
    #each player evaluates his hand, matching the highest bet or folding (TODO: raising)
    for i in PlayerList:
        #raising should be the first option (TODO)
        #Big Blind has already placed the bet, Little Blind figures why not 
        if i.betAmount == highestBet:
            pass
        elif i.betAmount == 5:
            i.betAmount = highestBet
            i.cash -= 5
        elif i.hand.startingHand() <= 8: 
            i.betAmount = highestBet
            i.cash -= i.betAmount        
        else:
            i.fold = True
            boardFunc.pot += i.betAmount
        

        
            
   
    for i in PlayerList:
        boardFunc.pot += i.betAmount
        i.betAmount = 0
        
        
        
        
    
    #deal to the board
    board = Hand(deck.draw(3))

    #board cards are (for practical purposes) added to players hands
    for i in PlayerList:
        if i.fold == False:
            i.hand = Hand(i.hand.cards + board.cards)

    #add another card to both the board and the hands
    drawOne = deck.draw(1)
    board.cards = board.cards + drawOne

    for i in PlayerList:
        if i.fold == False:
            i.hand = Hand(i.hand.cards + drawOne)

    #draw final card to board
    drawOne = deck.draw(1)

    #add it to both the board and the hands
    board.cards = board.cards + drawOne

    for i in PlayerList:
        if i.fold == False:
            i.hand = Hand(i.hand.cards + drawOne)
    
    #determining winning players will use two loops
    deck2 = Deck() #a dummy deck
    bestHand = Hand(deck2.draw(5)) #a dummy hand
    bestHand.value = -1 #can't win with this hand

    #establishes correspondence with highest ranking hand
    for i in PlayerList:
        if i.fold == False:
            if i.hand > bestHand:
                bestHand = i.hand
    
    #account for ties "==" does not work as class instances are being compared     
    for i in PlayerList:
        if i.fold == False:
            if i.hand < bestHand:
                pass
            else:
                i.hand.winner = True
    
    #count the number of winners and divide up the winnings
    winnerCount = 0
    for i in PlayerList:
        if i.hand.winner == True:
            winnerCount += 1
    if winnerCount > 1:
        boardFunc.ties += 1
        for i in PlayerList:
            if i.hand.winner == True:
                print (i.hand)

    #print ('winner count = ' + str(winnerCount))

    #if everyone folds there will be an error--there must be a winner
    boardFunc.pot = boardFunc.pot//winnerCount
    #print ('winnings = ' + str(boardFunc.pot))

    
    for i in PlayerList:
        if i.hand.winner == True:
            i.cash += boardFunc.pot
    #any remainder will stay in pot
    boardFunc.pot = boardFunc.pot%winnerCount
    #print ('left in pot = ' + str(boardFunc.pot))

    #constantTotal = 0
    #for i in PlayerList:
        #constantTotal += i.cash

    #print ('Running Total = ' + str(constantTotal))
    #for i in PlayerList:
        #print (round,i.personality,i.cash,i.hand.winner)
    #add round results into database    
    for i in PlayerList:
        #print(round,i.personality,i.hand,i.hand.winner,i.cash)
        c.execute("INSERT INTO hands VALUES(?,?,?,?,?,?,?)",
                  (round,
                   i.personality,
                   #str(i.hand),
                   i.hand.names[i.hand.value],
                   str(i.hand.best_cards),
                   i.hand.value,
                   i.hand.winner,
                   i.cash))
    
    round += 1
print (boardFunc.ties)
handsDb.commit()

#printing modules
from plotMethods import plotMethods

#prints entire database
plotMethod1 = plotMethods(c)
plotMethod1.allHands()

handsDb.close()

