import plotly.plotly as py

from plotly.graph_objs import *

import statistics as st


class plotMethods(object):
    def __init__(self, c_dataBase):
        self.c = c_dataBase

    def allHands(self):
        #count different types of hands 
        self.c.execute('SELECT hand, count(hand) FROM hands GROUP BY value')
        handData1 = self.c.fetchall()

        #count different types of winning hands
        self.c.execute("SELECT hand, count(hand) FROM hands WHERE won = '1' GROUP BY value")
        handData2 = self.c.fetchall()

        #count different winning players
        self.c.execute("SELECT player, count(player) FROM hands WHERE won = '1' GROUP BY player")
        handData3 = self.c.fetchall()

        #create lists of database output for graphs
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

        #create Bar Chart showing number of wins for each player
        trace3 = Bar(
            x = handType3,
            y = handFrequency3,
            name = 'Winning Players')

        #create bands representing 2 standard deviations from the mean to indicate significance
        stddev = []
        trace4Y = []
        for i in handType3:
                    stddev.append(st.pstdev(handFrequency3))
                    trace4Y.append(st.mean(handFrequency3))

        trace4 = Scatter(
            x = handType3,
            y = trace4Y,
            error_y = ErrorY(
                type = 'data',
                #2 std deviations   
                array = [2*x for x in stddev],
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




