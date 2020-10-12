import urllib.request
import os
import time


class Updater:

    def __init__(self, wallet_adr, dir_adr):
        self.data = dir_adr
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
        if not os.path.exists("\\CryptZ"):
            os.mkdir("\\CryptZ")
            # creates directory for external files if it doesn't exist
        if not os.path.exists(self.data):
            urllib.request.urlretrieve(self.__URLlink, self.data)
        elif time.time() - os.path.getmtime(self.data) > 86400:
            urllib.request.urlretrieve(self.__URLlink, self.data)
        # updates info if day passe


a = Updater("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "\\CryptZ\\Gemini_BTCUSD_d.csv")
a.updateLatestDownloadedDate()




