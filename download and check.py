import urllib.request
import os
import time
import pandas as pd
import datetime
import plotly.express as px
from abc import ABCMeta, abstractmethod, abstractproperty
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from fg import *
from statsmodels.tsa.arima_model import ARIMA
#dependencies for the DecisionTree method
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import numpy as np



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


class Plot:
    def __init__(self, df):
        self.df = df
        self.fig = ''
        self.img = ''
        #get an appropriate part of table

    def drawPlot(self): #draw a line based plot
        self.fig = px.line(self.df, x='Date', y='Close', width=990, height=335) #x:date; y:price
        self.fig.write_image("CryptZ\\fig3.png")

    def mixing(self):
        fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
                     hover_data=['Volume_BTC', 'Volume_USD'],
                     title='Evolution')
        fig.show() #x:Date; y:Price; color:Volume; prompted_data:'Volume_BTC', 'Volume_USD'
        #fig.write_image("OOP_\\images\\fig3.png", engine = 'kaleido')

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
            urllib.request.urlretrieve(self.__URLlink, self.data)     # updates info if day is passed
        with open(self.getFilename(), "r") as file:
            lines = file.readlines()
            if lines[0][:4] != "Unix":
                del lines[0]
                with open(self.getFilename(), "w+") as new_file:
                    for line in lines:
                        new_file.write(line)


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

            return RangeError("Incorrect values").ShowError()


class History:#Singletone
    __instance = None
    def __new__(cls, dir_adr, name, minDate, maxDate):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, dir_adr, name, minDate, maxDate):
        self.curRange = Data(dir_adr, name, minDate, maxDate)
        self.minDate = minDate
        self.maxDate = maxDate
        self.name = name

    def getrange(self):
        return self.curRange.getDataRange()

    def getStartDate(self):
        return self.minDate

    def getEndDate(self):
        return self.maxDate

class CustomExeption(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Error:
    __metaclass__ = ABCMeta

    @abstractmethod
    def ShowError(self):
        pass


class RangeError(Error):
    def __init__(self, message):
        self.message = message

    def ShowError(self):
        print(self.message)

class Genie:
    def __init__(self, futute_days):
        self.__future_days = futute_days

        # variable to predict 'x' days

    def setDayPrediction(self, future_days):
        self.__future_days = future_days

    def predict_ml(self, df):
        df = df.iloc[::-1]  # reverse data-frame
        df = df[['Close']]
        future_days = 30  # variable to predict 'x' days
        df['Prediction'] = df[['Close']].shift(-future_days)
        df['Prediction'] = df[['Close']].shift(-self.__future_days)

        # creating a feature data set converted to numpy array without the last 'x' rows
        x = np.array(df.drop(['Prediction'], 1))[:-future_days]
        y = np.array(df['Prediction'])[:-future_days]
        x = np.array(df.drop(['Prediction'], 1))[:-self.__future_days]
        y = np.array(df['Prediction'])[:-self.__future_days]
        # Split the data for training and testing
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.0025)
        tree = DecisionTreeRegressor().fit(x_train, y_train)

        # Get the last 'x' rows from the feature data set
        x_future = df.drop(['Prediction'], 1)[:-future_days]
        x_future = x_future.tail(future_days)
        x_future = df.drop(['Prediction'], 1)[:-self.__future_days]
        x_future = x_future.tail(self.__future_days)
        x_future = np.array(x_future)
        # Show the model tree prediction
        tree_prediction = tree.predict(x_future)
        test = pd.DataFrame()
        test['Tree'] = tree_prediction
        # Create a current range
        start = datetime.date.today()
        date_generated = [start + datetime.timedelta(days=x) for x in range(future_days)]
        date_generated = [start + datetime.timedelta(days=x) for x in range(self.__future_days)]
        date_table = []
        for date in date_generated:
            date_table.append(date.strftime("%Y-%m-%d"))
        test['Date'] = date_table
        fig_p = px.line(test, x = 'Date', y = 'Tree', width=652, height=290) #x:date; y:price
        fig_p.write_image("CryptZ\\fig4.png")








a = Refresher("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "CryptZ\BTC__USD.csv", "BTC")

a.updateLatestDownloadedDate()


class Window(QtWidgets.QMainWindow, Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.Enddate.hide()
        self.Startdate.hide()
        self.Tabledate.hide()
        self.listWidget.hide()
        self.Tabledate.editingFinished.connect(self.table)
        self.setdate = ''
        self.plot = ''
        self.Submit.clicked.connect(self.history)
        self.Submit_2.clicked.connect(self.predictor)
        self.horizontalSlider.hide()
        self.horizontalSlider.valueChanged.connect(self.slider)
        self.horizontalSlider.setValue(20)


        #self.horizontalSlider.hide()
        #self.lineEdit.hide()
        #self.toolButton_Coin_3.clicked.connect(self.lineEdit.show())




    def table(self):
        self.setdate = History('CryptZ\BTC__USD.csv', 'BTC', datetime.datetime.strptime(self.Tabledate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date(),
                    datetime.datetime.strptime(self.Tabledate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date() + datetime.timedelta(days=31))
        self.setdate = self.setdate.getrange()
        listdate = self.setdate["Date"].tolist()
        listclose = self.setdate["Close"].tolist()
        self.lineEdit_Day.setText(str(listdate[0]))
        self.lineEdit_Day_2.setText(str(listdate[1]))
        self.lineEdit_Day_3.setText(str(listdate[2]))
        self.lineEdit_Day_4.setText(str(listdate[3]))
        self.lineEdit_Day_5.setText(str(listdate[4]))
        self.lineEdit_Day_6.setText(str(listdate[5]))
        self.lineEdit_Day_7.setText(str(listdate[6]))
        self.lineEdit_Day_8.setText(str(listdate[7]))
        self.lineEdit_Day_9.setText(str(listdate[8]))
        self.lineEdit_Day_10.setText(str(listdate[9]))
        self.lineEdit_Day_11.setText(str(listdate[10]))
        self.lineEdit_Day_12.setText(str(listdate[11]))
        self.lineEdit_Day_13.setText(str(listdate[12]))
        self.lineEdit_Day_14.setText(str(listdate[13]))
        self.lineEdit_Day_15.setText(str(listdate[14]))
        self.lineEdit_Day_16.setText(str(listdate[15]))
        self.lineEdit_Day_17.setText(str(listdate[16]))
        self.lineEdit_Day_18.setText(str(listdate[17]))
        self.lineEdit_Day_19.setText(str(listdate[18]))
        self.lineEdit_Day_20.setText(str(listdate[19]))
        self.lineEdit_Day_21.setText(str(listdate[20]))
        self.lineEdit_Day_22.setText(str(listdate[21]))
        self.lineEdit_Day_23.setText(str(listdate[22]))
        self.lineEdit_Day_24.setText(str(listdate[23]))
        self.lineEdit_Day_25.setText(str(listdate[24]))
        self.lineEdit_Day_26.setText(str(listdate[25]))
        self.lineEdit_Day_27.setText(str(listdate[26]))
        self.lineEdit_Day_28.setText(str(listdate[27]))
        self.lineEdit_Day_29.setText(str(listdate[28]))
        self.lineEdit_Day_30.setText(str(listdate[29]))
        self.lineEdit_Day_31.setText(str(listdate[30]))
        self.lineEdit_Value.setText(str(listclose[0]) + "$")
        self.lineEdit_Value_2.setText(str(listclose[1]) + "$")
        self.lineEdit_Value_3.setText(str(listclose[2]) + "$")
        self.lineEdit_Value_4.setText(str(listclose[3]) + "$")
        self.lineEdit_Value_5.setText(str(listclose[4]) + "$")
        self.lineEdit_Value_6.setText(str(listclose[5]) + "$")
        self.lineEdit_Value_7.setText(str(listclose[6]) + "$")
        self.lineEdit_Value_8.setText(str(listclose[7]) + "$")
        self.lineEdit_Value_9.setText(str(listclose[8]) + "$")
        self.lineEdit_Value_10.setText(str(listclose[9]) + "$")
        self.lineEdit_Value_11.setText(str(listclose[10]) + "$")
        self.lineEdit_Value_12.setText(str(listclose[11]) + "$")
        self.lineEdit_Value_13.setText(str(listclose[12]) + "$")
        self.lineEdit_Value_14.setText(str(listclose[13]) + "$")
        self.lineEdit_Value_15.setText(str(listclose[14]) + "$")
        self.lineEdit_Value_16.setText(str(listclose[15]) + "$")
        self.lineEdit_Value_17.setText(str(listclose[16]) + "$")
        self.lineEdit_Value_18.setText(str(listclose[17]) + "$")
        self.lineEdit_Value_19.setText(str(listclose[18]) + "$")
        self.lineEdit_Value_20.setText(str(listclose[19]) + "$")
        self.lineEdit_Value_21.setText(str(listclose[20]) + "$")
        self.lineEdit_Value_22.setText(str(listclose[21]) + "$")
        self.lineEdit_Value_23.setText(str(listclose[22]) + "$")
        self.lineEdit_Value_24.setText(str(listclose[23]) + "$")
        self.lineEdit_Value_25.setText(str(listclose[24]) + "$")
        self.lineEdit_Value_26.setText(str(listclose[25]) + "$")
        self.lineEdit_Value_27.setText(str(listclose[26]) + "$")
        self.lineEdit_Value_28.setText(str(listclose[27]) + "$")
        self.lineEdit_Value_29.setText(str(listclose[28]) + "$")
        self.lineEdit_Value_30.setText(str(listclose[29]) + "$")
        self.lineEdit_Value_31.setText(str(listclose[30]) + "$")

    def history(self):

        self.setdate = History('CryptZ/BTC__USD.csv', 'BTC', datetime.datetime.strptime(self.Startdate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date(),
                    datetime.datetime.strptime(self.Enddate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date())
        self.setdate = self.setdate.getrange()
        self.plot = Plot(self.setdate)
        self.plot.drawPlot()

        self.label.setPixmap(QtGui.QPixmap("CryptZ/fig3.png"))

    def predictor(self):
        histoy = History('CryptZ/BTC__USD.csv', 'BTC', datetime.date(2015, 12, 10), datetime.date(2020, 11, 15))

        ab = Genie(int(self.lineEdit.text()))
        ab.predict_ml(histoy.getrange())
        self.label_5.setPixmap(QtGui.QPixmap("CryptZ/fig4.png"))

    def slider(self):
        self.lineEdit.setText(str(self.horizontalSlider.value()))






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())




