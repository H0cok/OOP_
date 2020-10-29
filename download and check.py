import urllib.request
import os
import time
import pandas as pd
import datetime
import plotly.express as px
from statsmodels.tsa.arima_model import ARIMA

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

basic_input = UserInput(datetime.date(2016, 3, 4), datetime.date(2016, 3, 9), "BTC", "day")

class CryptData:
    def __init__(self, dir_adr, name):
        self.data = dir_adr
        self.name = name


class Refresher(CryptData):
    def __init__(self, wallet_adr, dir_adr, name):
        super().__init__(dir_adr, name)
        self.__URLlink = wallet_adr

    def setCurrencyLink(self, link):
        self.__URLlink = link

    def getCurrencyLink(self):
        return self.__URLlink

    def setFilename(self, data):
        self.data = data

    def getFilename(self):
        return self.data

    def updateLatestDownloadedDate(self):
        if not os.path.exists("CryptZ"):
            os.mkdir("CryptZ")
            # creates directory for external files if it doesn't exist
        if not os.path.exists(self.data):
            urllib.request.urlretrieve(self.__URLlink, self.data)
        elif time.time() - os.path.getmtime(self.data) > 86400:
            urllib.request.urlretrieve(self.__URLlink, self.data)
        # updates info if day passe


class Data(CryptData):
    def __init__(self, dir_adr, name, start, end, range = None, minDate = None, maxDate = None):
        super().__init__(dir_adr, name)
        self.df = pd.read_csv(dir_adr, usecols=['Close', 'Date', 'Volume BTC', 'Volume USD'])
        self.StartDate = start
        self.EndDate = end
        self.range = range
        self.minDate = datetime.date(int(self.df.iloc[-1].Date[0: 4]),
                                     int(self.df.iloc[-1].Date[5: 7]), int(self.df.iloc[-1].Date[8:]))
        self.maxDate = datetime.date(int(self.df.iloc[-0].Date[0: 4]),
                                     int(self.df.iloc[-0].Date[5: 7]), int(self.df.iloc[-0].Date[8:]))


    def getDataRange(self):
        if self.minDate < self.StartDate < self.EndDate < self.maxDate:
            down = self.df[self.df.Date == str(self.EndDate)].index[0]
            up = self.df[self.df.Date == str(self.StartDate)].index[0]
            self.range = self.df.iloc[down: up + 1][::]
            return self.range
        else:
            return False #some error message

class History:
    def __init__(self, dir_adr, name, minDate, maxDate):
        self.curRange = Data(dir_adr, name, minDate, maxDate)
        self.minDate = minDate
        self.maxDate = maxDate
        self.name = name
    def getrange(self):
        return self.curRange.getDataRange()

class Plot:
    def drawPlot(self, df, x_axys, y_axys): #draw a line based plot
        fig = px.line(df, x = x_axys, y = y_axys) #x:date; y:price
        fig.show()
        #fig.to_image(format="png", engine="kaleido")
        #fig.write_image("OOP_\\images\\fig1.png")

    # def mixing(self):
    #     fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
    #                  hover_data=['Volume_BTC', 'Volume_USD'],
    #                  title='Evolution')
    #     fig.show() #x:Date; y:Price; color:Volume; prompted_data:'Volume_BTC', 'Volume_USD'
    #     #fig.write_image("OOP_\\images\\fig3.png", engine = 'kaleido')


class Genie:
    def predict_val(self, df):
        #df = pd.read_csv('OOP_\\BTC__USD.csv', usecols=['Close', 'Date'], parse_dates=True)
        #df = df.dropna()#discard extra columns
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
        graph.drawPlot(test, 'Date', 'Predicted')
        # fig = px.line(test, x = 'Date', y = 'Predicted') #x:date; y:price
        # fig.show()

#a = Refresher("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "CryptZ\BTC__USD.csv", "BTC")
#a.updateLatestDownloadedDate()
f = History("OOP_\CryptZ\BTC__USD.csv", "BTC", datetime.date(2019, 11, 17), datetime.date(2020, 6, 5))
graph = Plot()
graph.drawPlot(f.getrange(), 'Date', 'Close')
prediction = Genie()
prediction.predict_val(f.getrange())