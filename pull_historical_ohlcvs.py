import ccxt
import json
import time
bfx = ccxt.bitfinex({'enableRateLimit': True})
count = 0
import datetime
from pathlib import Path



symbol = 'BTC/USD'
timeframe = '1h'
startdaysago = 30


towrite = []
def grab_ohlcvs( symbol, start_date ):
	global count, towrite
	ohlcvs = bfx.fetch_ohlcv(symbol, timeframe, start_date, 10000 )
	high = 0
	for ohlcv in ohlcvs:
		if ohlcv[0] > high:
			high = ohlcv[0]
		towrite.append(ohlcv)	
	count = count + 1
	

	if count <= 10:
		return grab_ohlcvs( symbol, high )
	else:
		with open(symbol.replace('/','') + '.json', 'a') as outfile:
			json.dump(towrite, outfile)
		return
now = datetime.datetime.now()
then = now - datetime.timedelta(days=startdaysago)
then = time.mktime(then.timetuple())
grab_ohlcvs( symbol, then )