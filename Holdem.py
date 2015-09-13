
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
    
Graph of cash on hand changes throughout game for each personality type
Statistically significant differences given personality type (std dev error bars)
Establish bet system (bets, pots, cash on hand, blinds) 
Develop graphical interface for ease of modifying personality traits and viewing results
Develop personality types and alterable traits

BUGS

Establishing winning player hands--first hand has atypical amount of wins
    problem with ties
    sol: determine proper loop/iteration method to sort based on items in player hand list


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

from deck import Deck
deck = Deck()

import sqlite3
handsDb = sqlite3.connect(":memory:")
c = handsDb.cursor()

#create database table
c.execute('''CREATE TABLE hands
            (round integer, player text, hand text, cards text, value integer, won text, cash real)''')

#start of main program--run simulation a number of times put results in database
round = 1
for _ in range(1000):

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
    
    
    
    #determining winning players will use two loops
    deck2 = Deck() #a dummy deck
    bestHand = Hand(deck2.draw(5)) #a dummy hand
    bestHand.value = -1 #can't win with this hand

    #establishes correspondence with highest ranking hand
    for i in PlayerList:
        if i.hand > bestHand:
            bestHand = i.hand
            
    for i in PlayerList:
        if i.hand == bestHand:
            i.hand.winner = True

    
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
    #self.names[self.value]----self.best_cards
    #handsDb.commit()
    
    
    
    
    round += 1

handsDb.commit()

#prints entire database
"""
for row in c.execute('SELECT * FROM hands ORDER BY round'):
        print (row)
"""


import plotly.plotly as py

from plotly.graph_objs import *

import statistics as st


#select hands and count different types
c.execute('SELECT hand, count(hand) FROM hands GROUP BY value')
handData1 = c.fetchall()

#select winning hands
c.execute("SELECT hand, count (hand) FROM hands WHERE won = '1' GROUP BY value")
handData2 = c.fetchall()

#select winning personality types
c.execute("SELECT player, count(player) FROM hands WHERE won = '1' GROUP BY player")
handData3 = c.fetchall()

handFrequency1 = []
handType1 = []
for i in handData1:
    handFrequency1.append(i[1])
    handType1.append(i[0])

handFrequency2 = []
handType2 = []
for i in handData2:
    handFrequency2.append(i[1])
    handType2.append(i[0])

handFrequency3 = []
handType3 = []
for i in handData3:
    handFrequency3.append(i[1])
    handType3.append(i[0])

trace3 = Bar(
    x = handType3,
    y = handFrequency3,
    name = 'Winning Players')

stddev = []
trace4Y = []
for i in handType3:
            stddev.append(st.stdev(handFrequency3))
            trace4Y.append(st.mean(handFrequency3))

trace4 = Scatter(
    x = handType3,
    y = trace4Y,
    error_y = ErrorY(
        type = 'data',   
        array = stddev,
        visible = True)
    )
            
            
data = Data([trace3,trace4])
"""


#bar chart for hand types
trace1 = Bar(
    x = handType1,
    y = handFrequency1,
    name = 'All Hands')
trace2 = Bar(
    x = handType2,
    y = handFrequency2,
    name = 'Winning Hands')
data = Data([trace1,trace2])
layout = Layout(barmode='stack')
"""
#fig = Figure(data=data, layout=layout)
#plot_url = py.plot(fig, filename='')
plot_url = py.plot(data, filename='')

  



handsDb.close()

