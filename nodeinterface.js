KEY = process.env.key
SECRET = process.env.secret

var ccxtpro = require('ccxtpro')
var ccxtbase = require('ccxt')

const base = new ccxtbase.bitfinex ({ enableRateLimit: true, "apiKey": KEY,
    "secret": SECRET})
const pro = new ccxtpro.bitfinex ({ enableRateLimit: true, "apiKey": KEY,
    "secret": SECRET})
async function fM(){
markets = await base.fetchMarkets()
symbols = []
for (var m in markets){
	if (markets[m]['info']['margin'] == true){
		symbols.push(markets[m]['symbol'])
	}
}
//console.log(symbols)
}
fM()
tickers = {}
async function doit(){
//for (var s in symbols){
        try {

            var ticker = await pro.watchTicker ('BCH/USD', {})
            tickers[ticker['symbol']] = ticker

            console.log (new Date (), ticker)
        } 
catch (e) {
            console.log (e)
            // stop the loop on exception or leave it commented to retry
            // throw e
        }
 //   }

try {
            const balance = await pro.watchBalance ({})
            console.log (new Date (), balance)
        } catch (e) {
            console.log (e)
            // stop the loop on exception or leave it commented to retry
            // throw e
        }
}


doit()