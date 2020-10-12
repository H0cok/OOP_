import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import datetime

if not os.path.exists("OOP_\\images"):
    os.mkdir("OOP_\\images")

class UserInput:
    state = True # the input-field doesn`t blocked
    def __init__(self, st_date, end_date, coin_inp, intervals = None, investments = None):
        self.startDate = st_date
        self.endDate = end_date
        self.coin = coin_inp
        self.granularity = intervals
        self.investments = investments

    def setStartDate(self, st_date):
        self.startDate = st_date

    def setEndDate(self, end_date):
        self.endDate = end_date

    def setCoin(self, coin_inp):
        self.coin = coin_inp

    def setGranularity(self, interval):
        self.granularity = interval

    def setInvestments(self, money):
        self.investments = money

    def setState(self, state_inp): #triggered by generate btn
        self.state = state_inp

basic_input = UserInput(datetime.date(2016, 23, 4), datetime.date(2016, 23, 9), "BTC", "day")

class MainDash:
    df = pd.read_csv('OOP_\\BTC__USD.csv', usecols=['Close', 'Date', 'Volume_BTC', 'Volume_USD'])

    def __init__(self, bt_bound, up_bound):
        #self.bt_bound = bt_bound
        #self.up_bound = up_bound
        filter1 = self.df[self.df.Date == up_bound].index[0]
        filter2 = self.df[self.df.Date == bt_bound].index[0]
        self.df = self.df.iloc[filter1-1 : filter2][::-1] #get an appropriate part of table

    def drawLineDash(self): #draw a line-graph
        fig = px.line(x = self.df.Date[::-1], y = self.df.Close[::-1]) #x:date; y:price
        fig.show()
        #fig.write_image("OOP_\\images\\fig1.png")

    def mixing(self):
        fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
                     hover_data=['Volume_BTC', 'Volume_USD'],
                     title='Evolution')
        fig.show() #x:Date; y:Price; color:Volume; prompted_data:'Volume_BTC', 'Volume_USD'
        #fig.write_image("OOP_\\images\\fig3.png", engine = 'kaleido')

graph = MainDash("2018-09-27", "2019-03-27")
graph.drawLineDash()
graph.mixing()



