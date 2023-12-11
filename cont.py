import os
import time

import pandas as pd

csv = pd.read_csv("./res.csv")

res = csv['0']

for i in range(0, len(res)):
    req = round(res[i]*2100)
    # os.system("locust -f locusttest.py -H http://172.16.101.165:30001 -u %s "
    #           "-r 20 --csv loadtest_%s --csv-full-history --headless -t 5m"
    #           % (req, i))
    os.system("locust -f locusttest.py -H http://192.168.144.100:30001 -u %s "
              "-r 20 --csv loadtest_%s --csv-full-history --headless -t 5m"
              % (req, i))
    time.sleep(20)


    