import urllib.request
import os
import time
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
from statsmodels.tsa.arima_model import ARIMA
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, LSTM

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
            print(CustomExeption("Your range is empty"))
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
        graph.drawPlot(test, 'Date', 'Predicted')
        # fig = px.line(test, x = 'Date', y = 'Predicted') #x:date; y:price
        # fig.show()
    # def predict_val_lstm(self, df):
    #     df = df.iloc[::-1]#reverse data-frame
    #
    #     train = df.iloc[:-30]
    #     valid = df.iloc[-30:]
    #
    #     scaler = MinMaxScaler(feature_range=(0, 1))
    #     scaled_data = scaler.fit_transform(df)
    #
    #     x_train, y_train = [], []
    #     for i in range(60,len(train)):
    #         x_train.append(scaled_data[i-60:i,0])
    #         y_train.append(scaled_data[i,0])
    #     x_train, y_train = np.array(x_train), np.array(y_train)
    #     x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    #
    #     # create and fit the LSTM network
    #     model = Sequential()
    #     model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    #     model.add(LSTM(units=50))
    #     model.add(Dense(1))
    #
    #     model.compile(loss='mean_squared_error', optimizer='adam')
    #     model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
    #
    #     # predicting 246 values, using past 60 from the train data
    #     inputs = df[len(df) - len(valid) - 60:].values
    #     inputs = inputs.reshape(-1, 1)
    #     inputs = scaler.transform(inputs)
    #     X_test = []
    #     for i in range(60, inputs.shape[0]):
    #         X_test.append(inputs[i - 60:i, 0])
    #     X_test = np.array(X_test)
    #
    #     X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #     closing_price = model.predict(X_test)
    #     closing_price = scaler.inverse_transform(closing_price)
    #
    #     rms = np.sqrt(np.mean(np.power((valid - closing_price), 2)))
    #     print(rms)

# a = Refresher("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "CryptZ\BTC__USD.csv", "BTC")
# a.updateLatestDownloadedDate()
try:
    f = History("CryptZ\\BTC__USD.csv", "BTC", datetime.date(2019, 11, 17), datetime.date(2019, 11, 17))
    graph = Plot()
    graph.drawPlot(f.getrange(), 'Date', 'Close')
    prediction = Genie()
    prediction.predict_val_arima(f.getrange())
except:
    print(CustomExeption("Graph can't be created\n"))