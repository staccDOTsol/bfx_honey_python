import strategies.SMA as SMA
import threading
from time import sleep
import json
import os
import sys
coin = 't' + str(sys.argv[1])

def stratLauncher(coin):
    

    with open(coin.replace('t','').replace('/','') + '.json', 'r') as outfile:
        temp = (outfile.read())
    temp = temp[:-1]
    temp = temp[1:]
    temp = temp.replace('][','],[')
    temp2 = json.loads(temp)
    with open(coin.replace('/','') + '.json', 'w') as outfile:
        json.dump(temp2, outfile)

    smaStrat = SMA.SMA (  coin  )
    smaStrat.run()
stratLauncher(coin)