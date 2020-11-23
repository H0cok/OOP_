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
        self.fig.to_image(format="png", width=881, height=21, scale=0.01)
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
        self.curDate = time.time()

    def getFileLink(self):
        return self.data

    def updateLatestDownloadedDate(self):
        if not os.path.exists("CryptZ"):
            os.mkdir("CryptZ")
            # creates directory for external files if it doesn't exist
        if not os.path.exists(self.data):
            urllib.request.urlretrieve(self.__URLlink, self.data)
        elif self.curDate - os.path.getmtime(self.data) > 86400: # date length in sec
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

            return RangeError("Incorrect values").ShowError()


class History:
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






basic_input = UserInput(datetime.date(2016, 3, 4), datetime.date(2016, 3, 9), "BTC", "day")


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



    def table(self):
        self.setdate = History('CryptZ\BTC__USD.csv', 'BTC', datetime.datetime.strptime(self.Tabledate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date(),
                    datetime.datetime.strptime(self.Tabledate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date() + datetime.timedelta(days=31))
        self.setdate = self.setdate.getrange()
        print(self.setdate)
        self.lineEdit_Day.setText(str(self.setdate["Date"].tolist()[0]))
        self.lineEdit_Day_2.setText(str(self.setdate["Date"].tolist()[1]))
        self.lineEdit_Day_3.setText(str(self.setdate["Date"].tolist()[2]))
        self.lineEdit_Day_4.setText(str(self.setdate["Date"].tolist()[3]))
        self.lineEdit_Day_5.setText(str(self.setdate["Date"].tolist()[4]))
        self.lineEdit_Day_6.setText(str(self.setdate["Date"].tolist()[5]))
        self.lineEdit_Day_7.setText(str(self.setdate["Date"].tolist()[6]))
        self.lineEdit_Day_8.setText(str(self.setdate["Date"].tolist()[7]))
        self.lineEdit_Day_9.setText(str(self.setdate["Date"].tolist()[8]))
        self.lineEdit_Day_10.setText(str(self.setdate["Date"].tolist()[9]))
        self.lineEdit_Day_11.setText(str(self.setdate["Date"].tolist()[10]))
        self.lineEdit_Day_12.setText(str(self.setdate["Date"].tolist()[11]))
        self.lineEdit_Day_13.setText(str(self.setdate["Date"].tolist()[12]))
        self.lineEdit_Day_14.setText(str(self.setdate["Date"].tolist()[13]))
        self.lineEdit_Day_15.setText(str(self.setdate["Date"].tolist()[14]))
        self.lineEdit_Day_16.setText(str(self.setdate["Date"].tolist()[15]))
        self.lineEdit_Day_17.setText(str(self.setdate["Date"].tolist()[16]))
        self.lineEdit_Day_18.setText(str(self.setdate["Date"].tolist()[17]))
        self.lineEdit_Day_19.setText(str(self.setdate["Date"].tolist()[18]))
        self.lineEdit_Day_20.setText(str(self.setdate["Date"].tolist()[19]))
        self.lineEdit_Day_21.setText(str(self.setdate["Date"].tolist()[20]))
        self.lineEdit_Day_22.setText(str(self.setdate["Date"].tolist()[21]))
        self.lineEdit_Day_23.setText(str(self.setdate["Date"].tolist()[22]))
        self.lineEdit_Day_24.setText(str(self.setdate["Date"].tolist()[23]))
        self.lineEdit_Day_25.setText(str(self.setdate["Date"].tolist()[24]))
        self.lineEdit_Day_26.setText(str(self.setdate["Date"].tolist()[25]))
        self.lineEdit_Day_27.setText(str(self.setdate["Date"].tolist()[26]))
        self.lineEdit_Day_28.setText(str(self.setdate["Date"].tolist()[27]))
        self.lineEdit_Day_29.setText(str(self.setdate["Date"].tolist()[28]))
        self.lineEdit_Day_30.setText(str(self.setdate["Date"].tolist()[29]))
        self.lineEdit_Day_31.setText(str(self.setdate["Date"].tolist()[30]))
        self.lineEdit_Value.setText(str(self.setdate["Close"].tolist()[0]) + "$")
        self.lineEdit_Value_2.setText(str(self.setdate["Close"].tolist()[1]) + "$")
        self.lineEdit_Value_3.setText(str(self.setdate["Close"].tolist()[2]) + "$")
        self.lineEdit_Value_4.setText(str(self.setdate["Close"].tolist()[3]) + "$")
        self.lineEdit_Value_5.setText(str(self.setdate["Close"].tolist()[4]) + "$")
        self.lineEdit_Value_6.setText(str(self.setdate["Close"].tolist()[5]) + "$")
        self.lineEdit_Value_7.setText(str(self.setdate["Close"].tolist()[6]) + "$")
        self.lineEdit_Value_8.setText(str(self.setdate["Close"].tolist()[7]) + "$")
        self.lineEdit_Value_9.setText(str(self.setdate["Close"].tolist()[8]) + "$")
        self.lineEdit_Value_10.setText(str(self.setdate["Close"].tolist()[9]) + "$")
        self.lineEdit_Value_11.setText(str(self.setdate["Close"].tolist()[10]) + "$")
        self.lineEdit_Value_12.setText(str(self.setdate["Close"].tolist()[11]) + "$")
        self.lineEdit_Value_13.setText(str(self.setdate["Close"].tolist()[12]) + "$")
        self.lineEdit_Value_14.setText(str(self.setdate["Close"].tolist()[13]) + "$")
        self.lineEdit_Value_15.setText(str(self.setdate["Close"].tolist()[14]) + "$")
        self.lineEdit_Value_16.setText(str(self.setdate["Close"].tolist()[15]) + "$")
        self.lineEdit_Value_17.setText(str(self.setdate["Close"].tolist()[16]) + "$")
        self.lineEdit_Value_18.setText(str(self.setdate["Close"].tolist()[17]) + "$")
        self.lineEdit_Value_19.setText(str(self.setdate["Close"].tolist()[18]) + "$")
        self.lineEdit_Value_20.setText(str(self.setdate["Close"].tolist()[19]) + "$")
        self.lineEdit_Value_21.setText(str(self.setdate["Close"].tolist()[20]) + "$")
        self.lineEdit_Value_22.setText(str(self.setdate["Close"].tolist()[21]) + "$")
        self.lineEdit_Value_23.setText(str(self.setdate["Close"].tolist()[22]) + "$")
        self.lineEdit_Value_24.setText(str(self.setdate["Close"].tolist()[23]) + "$")
        self.lineEdit_Value_25.setText(str(self.setdate["Close"].tolist()[24]) + "$")
        self.lineEdit_Value_26.setText(str(self.setdate["Close"].tolist()[25]) + "$")
        self.lineEdit_Value_27.setText(str(self.setdate["Close"].tolist()[26]) + "$")
        self.lineEdit_Value_28.setText(str(self.setdate["Close"].tolist()[27]) + "$")
        self.lineEdit_Value_29.setText(str(self.setdate["Close"].tolist()[28]) + "$")
        self.lineEdit_Value_30.setText(str(self.setdate["Close"].tolist()[29]) + "$")
        self.lineEdit_Value_31.setText(str(self.setdate["Close"].tolist()[30]) + "$")





        pass


    def history(self):
        print("55")
        self.setdate = History('CryptZ/BTC__USD.csv', 'BTC', datetime.datetime.strptime(self.Startdate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date(),
                    datetime.datetime.strptime(self.Enddate.date().toString(QtCore.Qt.ISODate), "%Y-%m-%d").date())
        self.setdate = self.setdate.getrange()
        self.plot = Plot(self.setdate)
        self.plot.drawPlot()
        self.label.setPixmap(QtGui.QPixmap("CryptZ/fig3.png"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())




