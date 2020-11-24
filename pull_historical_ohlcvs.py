import ccxt
import json
import time
from pypac import PACSession, get_pac

rate = 0.33# / 32
import random

import sys, linecache
def PrintException( exchange ):
    #if apiKey == firstkey:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    string = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    if 'connect timeout' not in string and 'Read timed out' not in string and 'requires string as left operand, not int' not in string and  'ERR_RATE_LIMIT' not in string:
        print(string)
    elif 'ERR_RATE_LIMIT' in string:
        exchange.acount = 100
    else:
        exchange.acount = 100
        
count = {}
import datetime
from pathlib import Path
from time import sleep

symbols = ['BTC/USD', 'LTC/USD', 'ETH/USD', 'ETC/USD', 'ZEC/USD', 'XMR/USD', 'DASH/USD', 'XRP/USD', 'IOTA/USD', 'EOS/USD', 'SAN/USD', 'OMG/USD', 'NEO/USD', 'ETP/USD', 'PNT/USD', 'BTG/USD', 'ZRX/USD', 'TRX/USD', 'DAI/USD', 'XLM/USD', 'XTZ/USD', 'BSV/USD', 'USDT/USD', 'ATOM/USD', 'LEO/USD', 'ALGO/USD', 'FTT/USD', 'XAUT/USD', 'DOT/USD', 'ADA/USD', 'LINK/USD', 'UNI/USD', 'YFI/USD', 'FIL/USD']
print(symbols)
#sleep(100)
symbol = 'BTC/USD'
timeframe = '1h'
startdaysago = 90

import threading
towrite = {}
rateBlock = {}
#from binance.protonvpn_cli.cli import proto2
#proton = proto2()

bfx = {}
masterproxies = {}
def resetBlock():
    global rateBlock
    sleep(0)
    #print('resetBlock')
    rateBlock[symbol] = False
returns = {}
class KillableThread(threading.Thread):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self._kill = threading.Event()

    def run(self):
        global count, towrite, rateBlock, returns, masterproxies, bfx
        symbol = self.symbol
        while True:
            try:
                #print(bfx[symbol].session.proxies )
                abc=123#masterproxies[symbol] = bfx[symbol].session.proxies2
            except Exception as e:
                #PrintException()
                abc=123#print(e)
                #sleep(5)
                #masterproxies = []
            try:
                try:
                    if bfx[symbol] == None:
                        print('new bfx...')
                        bfx[symbol] = ccxt.bitfinex({'enableRateLimit': False})#, 'masterproxies': masterproxies})#, 'rateLimit': 680})
                        
                        bfx[symbol].load_markets()
                except:
                    
                    print('new bfx...')
                    try:
                        bfx[symbol] = ccxt.bitfinex({'enableRateLimit': False})#, 'masterproxies': masterproxies})#, 'rateLimit': 680})
                        
                        
                        bfx[symbol].load_markets()
                    except:
                        PrintException( bfx[symbol] )
                        abc=123
                        #bfx[symbol].session._tried_get_pac = False
                        #pac = get_pac(url="http://localhost/proxies.PAC")
                        #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

                        #bfx[symbol].session._proxy_resolver = None
                        #bfx[symbol].session.resetResolver(pac)
                        #bfx[symbol].session._proxy_resolver.unban_all()
                #print('mp')
                #print(masterproxies)
                #bfx[symbol].masterproxies = masterproxies
                start_date = returns[symbol]
                try:
                    a = (len(towrite[symbol]))
                    
                    towrite[symbol] = []
                except:
                    towrite[symbol] = []
                    count[symbol] = 0
                    with open(symbol.replace('/','') + '.json', 'w') as outfile:
                        outfile.write('"[')
                #with open(symbol.replace('/','') + '.json', 'r') as outfile:
                #    towrite[symbol] = json.loads(outfile.read())
                
                if rateBlock[symbol] == False:
                    try:
                        rateBlock[symbol] = True
                        #print(symbol)
                        #sleep(1)
                        #print('')
                        
                             
                        
                        #print('')
                        ohlcvs = bfx[symbol].fetch_ohlcv(symbol, timeframe, start_date, 1000 )
                        
                        t = threading.Thread(target=resetBlock)
                        t.daemon = True
                        t.start()
                        #print('setrateBlock[symbol]')
                        high = 0
                        for ohlcv in ohlcvs:
                            if ohlcv[0] > high:
                                high = ohlcv[0]
                            towrite[symbol].append(ohlcv)    
                        count[symbol] = count[symbol] + 1
                        
                        if 'BTC' in symbol:
                            print(count)
                            
                        temp = str(towrite[symbol])
                        temp = temp[:-1]
                        temp = temp[1:]
                        if count[symbol] >= 10:#10:
                            count[symbol] = 0
                            with open(symbol.replace('/','') + '.json', 'a') as outfile:
                                outfile.write(temp)
                            returns[symbol] = high
                            rateBlock[symbol] = False
                        if len(ohlcvs) < 1000 - 10:
                            with open(symbol.replace('/','') + '.json', 'a') as outfile:
                                outfile.write(temp + ']"')
                            returns[symbol] = 0
                            rateBlock[symbol] = False
                            break
                    except Exception as e:
                        if 'requires string as left operand, not int' in str(e):
                            bfx[symbol] = ccxt.bitfinex({'enableRateLimit': False})#, ' 'rateLimit': 680})
                        
                        
                            bfx[symbol].load_markets()  
                        #if 'BTC' in symbol:
                            #PrintException( bfx[symbol] )
                       # print(e)
                        #proton.connect()
                        
                        
                        #bfx[symbol].session._tried_get_pac = False
                        #pac = get_pac(url="http://localhost/proxies.PAC")
                        #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

                        #bfx[symbol].session._proxy_resolver = None
                        #bfx[symbol].session.resetResolver(pac)
                        #bfx[symbol].session._proxy_resolver.unban_all()
                        rate = random.randint(1,3)/10
                        sleep(rate)
                        #with open(symbol.replace('/','') + '.json', 'a') as outfile:
                        #    json.dump(towrite[symbol], outfile)
                        returns[symbol] = start_date
                        rateBlock[symbol] = False
                else:
                    #print('sleeping...')
                    rate = random.randint(1,3)/10
                    sleep(rate)
                    #with open(symbol.replace('/','') + '.json', 'a') as outfile:
                    #    json.dump(towrite[symbol], outfile)
                    returns[symbol] = start_date
                    rateBlock[symbol] = False
            except Exception as e:
                
                PrintException(bfx[symbol])
                #bfx[symbol].session._tried_get_pac = False
                #pac = get_pac(url="http://localhost/proxies.PAC")
                #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

                #bfx[symbol].session._proxy_resolver = None
                #bfx[symbol].session.resetResolver(pac)
                #bfx[symbol].session._proxy_resolver.unban_all()
                rate = random.randint(1,3)/10
                sleep(rate)
                rateBlock[symbol] = False
            rate = random.randint(1,3)/10
            is_killed = self._kill.wait(rate)
            if is_killed:
                break

       # print("Killing Thread")

    def kill(self):
        self._kill.set()

            
now = datetime.datetime.now()
then = now - datetime.timedelta(days=startdaysago)
then = time.mktime(then.timetuple())

num = threading.activeCount()
print(num)
ts = {}
symcount = 0
symt = len(symbols)
runningSyms = []
symbol = None
oldsymbol = None
while symcount < len(symbols):
    
    if threading.activeCount() <= num + 8 and symcount < len(symbols):
        if threading.activeCount() > num + 8:#len(ts) > 0:
            for symbol in runningSyms:
                if returns[symbol] == 0:
                    runningSyms.remove(symbol)
                    
                    ts[symbol].kill()
        #print(oldsymbol)
        if oldsymbol != None:
            try:
                if len(bfx[oldsymbol].proxies) > 0:
                    """
                    try:
                        #print(bfx[oldsymbol].session.proxies2)
                        masterproxies[oldsymbol] = bfx[oldsymbol].session.proxies2
                        bfx[symbol].masterproxies = masterproxies
                    except Exception as e:
                        #PrintException()
                        abc=123#print(e)
                    """
                    oldsymbol = symbol
                    symbol = symbols[symcount]
                    symcount = symcount + 1 
                    returns[symbol] = then
                    runningSyms.append(symbol)
                    
                    print('0')
                    print(symbol)
                    rateBlock[symbol] = False
                    t = t = KillableThread(symbol=symbol)
                    
                    t.daemon = True
                    #ts.append(t)
                    t.start()
                    
                    ts[symbol] = t
                    sleep(1)
            except:
            
                
                sleep(1)
        else:
            symbol = symbols[symcount]
            oldsymbol = symbol
            symcount = symcount + 1 
            returns[symbol] = then
            runningSyms.append(symbol)
            print('1')
            print(symbol)
            rateBlock[symbol] = False
            t = t = KillableThread(symbol=symbol)
            
            t.daemon = True
            #ts.append(t)
            t.start()
            
            ts[symbol] = t
            sleep(1)

        #sleep(5)
    else:
        print('thread activecount: ' + str(threading.activeCount()) + ', lenrunningSyms: ' + str(len(runningSyms)))
        sleep(5)
while threading.activeCount() > num:
    print('thread activecount: ' + str(threading.activeCount()) + ', lenrunningSyms: ' + str(len(runningSyms)))
    sleep(5)