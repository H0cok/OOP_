import urllib.request
import os
import time


class Updater:
    this_day = time.asctime()
    def __init__(self, wallet_adr, dir_adr):
        self.data = dir_adr
        self.__URLlink = wallet_adr

    def updateLastDownloadedDate(self):
        if not os.path.exists(os.path.join("OOP_\\CryptZ")):
            os.mkdir(os.path.join("OOP_\\CryptZ"))
            # creates directory for external files if it doesn't exist
        else:
            timefile = open(self.__BTC_time_path, "r+")
            if timefile.read(7) != self.this_day[0:7]:
                timefile.truncate(0)
                timefile.seek(0)
                timefile.write(self.this_day)
                urllib.request.urlretrieve(self.__URLlink,
                                           Updater.data)
            timefile.close()
        # updates info if day passe
a = Updater("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv", "OOP_\\CryptZ\\Bitcoindata.csv")
a.updateLastDownloadedDate()




