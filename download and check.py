import urllib.request
import os
import time

if not os.path.exists(os.path.join("C:\\", "Program Files", "CryptZ")):
    os.mkdir(os.path.join("C:\\", "Program Files", "CryptZ"))
    # creates directory for external files if it doesn't exist

if not os.path.exists(os.path.join("C:\\", "Program Files", "CryptZ", "lastupdateBTC.txt")):
    timefile = open("C:\Program Files\CryptZ\lastupdateBTC.txt", "w", encoding= "utf-8")
    timefile.write(time.asctime())
    timefile.close()
    urllib.request.urlretrieve("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv",
                               "C:\Program Files\CryptZ\Bitcoindata.csv")
    # сreates a file with time of last update if it doesn't exist
else:
    timefile = open("C:\Program Files\CryptZ\lastupdateBTC.txt", "r+")
    this_day = time.asctime()
    if timefile.read(7) != this_day[0:7]:
        timefile.truncate(0)
        timefile.seek(0)
        timefile.write(this_day)
        urllib.request.urlretrieve("https://www.cryptodatadownload.com/cdd/Gemini_BTCUSD_d.csv",
                                   "C:\Program Files\CryptZ\Bitcoindata.csv")
    timefile.close()
    # updates info if day passed





