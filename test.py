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
        else: # date length in sec
            urllib.request.urlretrieve(self.__URLlink, self.data)
a = Refresher("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "CryptZ\BTC__USD.csv", "BTC")

a.updateLatestDownloadedDate()