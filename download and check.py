import urllib.request
import os
import time
import pandas as pd
import datetime
from abc import ABCMeta, abstractmethod, abstractproperty


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

f = History('CryptZ\BTC__USD.csv', 'BTC', datetime.date(2019, 11, 17), datetime.date(2020, 7, 5))
print(f.getrange())




