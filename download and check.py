import urllib.request
import os
import time
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
from statsmodels.tsa.arima_model import ARIMA
#dependencies for the DecisionTree method
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split



class UserInput:
    state = True # the input-field doesn`t blocked
    def __init__(self, st_date, end_date, coin_inp, intervals = None, investments = None):
        self.__startDate = st_date
        self.__endDate = end_date
        self.__coin = coin_inp
        self.__granularity = intervals
        self.__investments = investments

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

class CustomExeption(Exception):
    def __init__(self, msg):
        super().__init__(msg)

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
            raise CustomExeption("Your range is empty")
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
        fig.to_image(format="png", engine="kaleido")
        fig.write_image("images\\fig1.png")

    # def mixing(self):
    #     fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
    #                  hover_data=['Volume_BTC', 'Volume_USD'],
    #                  title='Evolution')
    #     fig.show() #x:Date; y:Price; color:Volume; prompted_data:'Volume_BTC', 'Volume_USD'
    #     #fig.write_image("OOP_\\images\\fig3.png", engine = 'kaleido')


class Genie:
    def __init__(self, futute_days):
        self.__future_days = futute_days # variable to predict 'x' days

    def setDayPrediction(self, future_days):
        self.__future_days = future_days

    def predict_ml(self, df):
        df = df.iloc[::-1] # reverse data-frame
        df = df[['Close']]
        df['Prediction'] = df[['Close']].shift(-self.__future_days)

        #creating a feature data set converted to numpy array without the last 'x' rows
        x = np.array(df.drop(['Prediction'], 1))[:-self.__future_days]
        y = np.array(df['Prediction'])[:-self.__future_days]
        #Split the data for training and testing
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1)
        tree = DecisionTreeRegressor().fit(x_train, y_train)

        #Get the last 'x' rows from the feature data set
        x_future = df.drop(['Prediction'], 1)[:-self.__future_days]
        x_future = x_future.tail(self.__future_days)
        x_future = np.array(x_future)
        #Show the model tree prediction
        tree_prediction = tree.predict(x_future)
        test = pd.DataFrame()
        test['Tree'] = tree_prediction
        #Create a current range
        start = datetime.date.today()
        date_generated = [start + datetime.timedelta(days=x) for x in range(self.__future_days)]
        date_table = []
        for date in date_generated:
            date_table.append(date.strftime("%Y-%m-%d"))
        test['Date'] = date_table
        print(test)
        #Visualizing the data
        graph.drawPlot(test, 'Date', 'Tree')

    def predict_val_arima(self, df):
        df = df.iloc[::-1]#reverse data-frame

        #divide to test and train sections
        train = df.iloc[:-30]
        test = df.iloc[-30:]

        model = ARIMA(train['Close'], order=(2,2,1)) #order use best-model
        model = model.fit()
        start = len(train)
        end = len(train)+len(test)-1
        pred = model.predict(start=start, end=end, typ = 'levels')
        pred = pred.to_list()
        test['Predicted'] = pred
        print(test)
        #graph.drawPlot(test, 'Date', 'Predicted')

try:
    a = Refresher("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "CryptZ\BTC__USD.csv", "BTC")
    a.updateLatestDownloadedDate()
    f = History("CryptZ\\BTC__USD.csv", "BTC", datetime.date(2016, 11, 17), datetime.date(2020, 11, 19))
    graph = Plot()
    prediction = Genie(30)
    prediction.predict_ml(f.getrange())
except CustomExeption as e:
    print(e)