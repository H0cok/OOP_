import pandas as pd
import os
import plotly.express as px
import datetime
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import warnings
warnings.filterwarnings("ignore")

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

basic_input = UserInput(datetime.date(2016, 4, 23), datetime.date(2016, 9, 23), "BTC", "day")

class Plot:
    df = pd.read_csv('OOP_\\BTC__USD.csv', usecols=['Close', 'Date', 'Volume_BTC', 'Volume_USD'])

    def __init__(self, bt_bound, up_bound):
        filter1 = self.df[self.df.Date == up_bound].index[0]
        filter2 = self.df[self.df.Date == bt_bound].index[0]
        self.df = self.df.iloc[filter1-1 : filter2][::-1] #get an appropriate part of table

    def drawPlot(self): #draw a line based plot
        fig = px.line(self.df, x = 'Date', y = 'Close') #x:date; y:price
        fig.show()
        fig.to_image(format="png", engine="kaleido")
        fig.write_image("OOP_\\images\\fig1.png")

    def mixing(self):
        fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
                     hover_data=['Volume_BTC', 'Volume_USD'],
                     title='Evolution')
        fig.show() #x:Date; y:Price; color:Volume; prompted_data:'Volume_BTC', 'Volume_USD'
        #fig.write_image("OOP_\\images\\fig3.png", engine = 'kaleido')

graph = Plot("2018-09-27", "2019-03-27")
#graph.drawPlot()
#graph.mixing()

class Genie:
    # def best_model(self, df):
    #     self.ad_test(df['Close'])
    #     wise_step = auto_arima(df['Close'], trace = True, suppress_warnings = True)
    #     wise_step.summary()

    def predict_val(self):
        df = pd.read_csv('OOP_\\BTC__USD.csv', usecols=['Close', 'Date', 'Volume_BTC', 'Volume_USD'], parse_dates=True)
        df = df.dropna()#discard extra columns
        df = df.iloc[::-1]#reverse data-frame

        #divide to test and train sections
        train = df.iloc[:-30]
        test = df.iloc[-30:]

        model = ARIMA(train['Close'], order=(1,1,0)) #order use best-model
        model = model.fit()
        start = len(train)
        end = len(train)+len(test)-1
        pred = model.predict(start=start, end=end, typ = 'levels')
        pred = pred.to_list()
        test['Predicted'] = pred
        print(test)
        fig = px.line(test, x = 'Date', y = 'Predicted') #x:date; y:price
        fig.show()

prediction = Genie()
prediction.predict_val()