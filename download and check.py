import urllib.request
import os
import time


class Updater:
    BTC_data_cvs = "C:\Program Files\CryptZ\Bitcoindata.csv"
    def __init__(self):
        self.__timefile = None
        self.__BTC_time_path = "C:\Program Files\CryptZ\lastupdateBTC.txt"
        self.__this_day = ''
        self.__URLlink = "https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv"

    def update(self):
        if not os.path.exists(os.path.join("C:\\", "Program Files", "CryptZ")):
            os.mkdir(os.path.join("C:\\", "Program Files", "CryptZ"))
            # creates directory for external files if it doesn't exist

        if not os.path.exists(os.path.join("C:\\", "Program Files", "CryptZ", "lastupdateBTC.txt")):
            self.__timefile = open(self.__BTC_time_path, "w", encoding="utf-8")
            self.__timefile.write(time.asctime())
            self.__timefile.close()
            urllib.request.urlretrieve(self.__URLlink,
                                       Updater.BTC_data_cvs)
            # сreates a file with time of last update if it doesn't exist
        else:
            timefile = open(self.__BTC_time_path, "r+")
            this_day = time.asctime()
            if timefile.read(7) != this_day[0:7]:
                timefile.truncate(0)
                timefile.seek(0)
                timefile.write(this_day)
                urllib.request.urlretrieve(self.__URLlink,
                                           Updater.BTC_data_cvs)
            timefile.close()
        # updates info if day passe
a = Updater()
a.update()




