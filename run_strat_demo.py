#import strategies.EMA as EMA

#emaStrat = EMA.EMA ( 'tBTCUSD'  )
import strategies.SMA as SMA
import threading
from time import sleep
import json
import os
import subprocess


"""
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
"""
coins = []
for filename in os.listdir('./'):
    if filename.endswith(".json"): 
        coins.append(filename)
        continue
    else:
        continue
#sleep(1000)
while len(coins) > 0:
    coin = coins[0]#, 'tIOTAUSD', 'tXRPUSD', 'tIOTAUSD']:
    
    print(threading.activeCount())
    #sleep(5)
    if threading.activeCount() <= 8:
        #t = threading.Thread(target=stratLauncher, args=(coin,))
        #t.daemon = True
        #t.start()
        subprocess.Popen(["python","run_strat_demo2.py",coin])

        coins.remove(coin)
while threading.activeCount() > 0:
    print(threading.activeCount())
    sleep(5)