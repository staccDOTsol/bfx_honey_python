import argparse, logging, math, os, pathlib, sys, time, traceback
import threading
import ccxtpro
import asyncio
import ccxt
import linecache
from time import sleep
import threading
from cryptofeed import FeedHandler
from cryptofeed.callback import BookCallback, TickerCallback, TradeCallback
from cryptofeed.defines import BID, ASK, FUNDING, L2_BOOK, OPEN_INTEREST, TICKER, TRADES
from cryptofeed.exchanges import Bitfinex
fh = FeedHandler()

honeybot = None

KEY = os.environ['key']
SECRET = os.environ['secret']

async def ticker(feed, pair, bid, ask, timestamp, ex):
    
    #print(f'Ex?: {ex} Timestamp: {timestamp} Feed: {feed} Pair: {pair} Bid: {bid} Ask: {ask}')

    pair = pair.replace('-','/')
    if 'BAB' in pair:
        #print(symbol)
        pair = pair.replace('BAB', 'BCH')
    if 'DSH' in pair:
        pair = pair.replace('DSH', 'DASH')
    if 'EDO' in pair:
        pair = pair.replace('EDO', 'PNT')
    if 'UST' in pair:
        pair = pair.replace('UST', 'USDT')
    #if 'BCH' in pair:
        #print(pair)
   # print(feed + '-' + name + '-' + dt +': ' + str( 0.5 * ( float(bid) + float(ask))))
    honeybot.mids[pair] = 0.5 * ( float(ask) + float(bid))
    honeybot.bids[pair] = float(bid)
    honeybot.asks[pair] = float(ask) 
async def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    string = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print   (string)
    if 'ERR_RATE_LIMIT' in string:
        os.system("protonvpn c --cc NL")
        sleep(5)

class HoneyBot( object ):
    
    def __init__( self ):
        self.exchange = None
        self.ccxtbase = None
        self.ids = []
        self.symbols = []
        self.bids = {}
        self.asks = {}
        self.mids = {}
        self.bals = {}
    

    async def balance(self, loop):
        


        
        
        while True:
            try:
                
                
                balance = await self.exchange.watch_balance({})
                bals = (self.exchange.bals)
                done = 0
                #print(bals)
                #print(self.mids)
                while done < len(bals):
                    for bal in bals:
                        if bal in self.mids:
                            print(bal)
                            self.bals[bal] = bals[bal] * self.mids[bal]
                            done = done + 1
                    sleep(1)        
                t = 0
                print(self.bals)
                for bal in self.bals:
                    t = t + self.bals[bal]
                self.bals['total'] = t
                print(self.bals['total'])
                    

            except Exception as e:
                if "object has no attribute 'values'" not in str(e):
                    await PrintException()
                    sleep(5)
                else:
                    #await PrintException()
                    sleep(1)
            print('orders')
            try:
                orders = await self.exchange.watch_orders({})
                print(self.exchange.orders) 
            except:
                await PrintException()
            print('positions')
            try:
                positions = await self.exchange.watch_positions({})
                print(self.exchange.positions)
  
            except:
                await PrintException()
            print('margin')
            try:
                margin = await self.exchange.watch_margin({})
                print(self.exchange.margin)
 
            except:
                await PrintException()
            print('my_trades')
            try:
                my_trades = await self.exchange.watch_my_trades({})
                print(self.exchange.my_trades)

            except:
                await PrintException()
        await exchange.close()    
    def cancelall( self ):
        abc=123

    def runfirst( self ):
        #print([sys.executable] + sys.argv)
        #os.execv( '/usr/local/bin/protonvpn', ['protonvpn', 'c', '--cc', 'NL'] )
        #sleep(5)
        self.ccxtbase = ccxt.bitfinex({'enableRateLimit': True, "apiKey": KEY,
    "secret": SECRET})

        try:
            tickers = self.ccxtbase.fetchMarkets()

            for t in tickers:
                if t['info']['margin'] == True:
                    if 'USD' in t['id'] and 'TEST' not in t['id']: ## TODO: testing, remove this line
                        self.symbols.append(t['symbol'])
                        #print(t)
                        #split = len(t['base'])
                        #if 'BTC' in symbol['symbol']:
                            #print(symbol['symbol'])
                        normalized = t['id'][:-3] + '-USD'
                        
                        #normalized = normalized.replace(':', '')
                        if 'UST-USD' == normalized:
                            normalized = 'USDT-USD'
                        self.ids.append(normalized)
        except Exception as e:
            print(e)
            self.symbols = ['BTC/USD', 'LTC/USD', 'ETH/USD', 'ETC/USD', 'ZEC/USD', 'XMR/USD', 'DASH/USD', 'XRP/USD', 'IOTA/USD', 'EOS/USD', 'SAN/USD', 'OMG/USD', 'NEO/USD', 'ETP/USD', 'PNT/USD', 'BTG/USD', 'ZRX/USD', 'TRX/USD', 'DAI/USD', 'XLM/USD', 'XTZ/USD', 'BSV/USD', 'BCH/USD', 'USDT/USD', 'ATOM/USD', 'LEO/USD', 'ALGO/USD', 'FTT/USD', 'XAUT/USD', 'DOT/USD', 'ADA/USD', 'LINK/USD', 'UNI/USD']
            self.ids = ['BTC-USD', 'LTC-USD', 'ETH-USD', 'ETC-USD', 'ZEC-USD', 'XMR-USD', 'DSH-USD', 'XRP-USD', 'IOT-USD', 'EOS-USD', 'SAN-USD', 'OMG-USD', 'NEO-USD', 'ETP-USD', 'EDO-USD', 'BTG-USD', 'ZRX-USD', 'TRX-USD', 'DAI-USD', 'XLM-USD', 'XTZ-USD', 'BSV-USD', 'BAB-USD', 'USDT-USD', 'ATO-USD', 'LEO-USD', 'ALG-USD', 'FTT-USD', 'XAUT:-USD', 'DOT-USD', 'ADA-USD', 'LINK:-USD', 'UNI-USD']

        print(self.symbols)
        print(self.ids)
        config = {TICKER: self.ids}
        fh.add_feed(Bitfinex(config=config, callbacks={TICKER: TickerCallback(ticker)}))
        t = threading.Thread(target=self.fhrun, args=())
        t.daemon = True
        t.start()
        loop = asyncio.new_event_loop()
        self.exchange = ccxtpro.bitfinex({'enableRateLimit': True, 'asyncio_loop': loop, "apiKey": KEY,
    "secret": SECRET})
        #ticker = self.exchange.fetchTicker('BCH/USD')
        
        loop.run_until_complete(self.balance(loop))
    def fhrun( self ):
        while True:
            fh.run()
            sleep(2)
    def run( self ):
        self.runfirst()
    def restart( self, msg=None ):
        try:
            strMsg = 'RESTARTING'
            print( strMsg )
            self.cancelall()
            strMsg += ' '
            for i in range( 0, 5 ):
                strMsg += '.'
                print( strMsg )
                sleep( 5 )
        except:
            pass
        finally:
        
            os.system("protonvpn c --cc NL")
            sleep(5)
            os.execv( sys.executable, [ sys.executable ] + sys.argv )  

if __name__ == '__main__':
    
    try:                                                
        honeybot = HoneyBot( )
        honeybot.run()
    except( KeyboardInterrupt, SystemExit ):
        print( "Cancelling open orders" )
        honeybot.cancelall()
        sys.exit()
    except:
        print( traceback.format_exc())
         
        honeybot.restart(str(traceback.format_exc()))
