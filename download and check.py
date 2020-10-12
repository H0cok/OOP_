import urllib.request
import os
import time


class Refresher:
    curDate = time.time()

    def __init__(self, wallet_adr, dir_adr):
        self.data = dir_adr
        self.__URLlink = wallet_adr

    def getFileLink(self):
        return self.data

    def updateLatestDownloadedDate(self):
        if not os.path.exists("\\CryptZ"):
            os.mkdir("\\CryptZ")
            # creates directory for external files if it doesn't exist
        if not os.path.exists(self.data):
            urllib.request.urlretrieve(self.__URLlink, self.data)
        elif self.curDate - os.path.getmtime(self.data) > 86400: # date length in sec
            urllib.request.urlretrieve(self.__URLlink, self.data)
        # updates info if day passe


a = Refresher("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "\\CryptZ\\Gemini_BTCUSD_d.csv")
a.updateLatestDownloadedDate()




