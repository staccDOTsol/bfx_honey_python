"use strict";

//-----------------------------------------------------------------------------

const ccxt = require ('ccxt')
    , { deepExtend } = ccxt
    , Exchange  = require ('./js/base/Exchange')
    , { unique } = require ('ccxt/js/base/functions')
    // , errors    = require ('ccxt/js/base/errors')

//-----------------------------------------------------------------------------
// this is updated by vss.js when building

const version = '0.4.22'

// Exchange.ccxtVersion = version

//-----------------------------------------------------------------------------

const exchanges = {
    'bequant':                 require ('./js/bequant.js'),
    'binance':                 require ('./js/binance.js'),
    'binanceje':               require ('./js/binanceje.js'),
    'binanceus':               require ('./js/binanceus.js'),
    'bitfinex':                require ('./js/bitfinex.js'),
    'bitmex':                  require ('./js/bitmex.js'),
    'bitstamp':                require ('./js/bitstamp.js'),
    'bittrex':                 require ('./js/bittrex.js'),
    'bitvavo':                 require ('./js/bitvavo.js'),
    'coinbaseprime':           require ('./js/coinbaseprime.js'),
    'coinbasepro':             require ('./js/coinbasepro.js'),
    'currencycom':             require ('./js/currencycom.js'),
    'ftx':                     require ('./js/ftx.js'),
    'gateio':                  require ('./js/gateio.js'),
    'hitbtc':                  require ('./js/hitbtc.js'),
    'huobijp':                 require ('./js/huobijp.js'),
    'huobipro':                require ('./js/huobipro.js'),
    'huobiru':                 require ('./js/huobiru.js'),
    'idex2':                   require ('./js/idex2.js'),
    'kraken':                  require ('./js/kraken.js'),
    'kucoin':                  require ('./js/kucoin.js'),
    'okcoin':                  require ('./js/okcoin.js'),
    'okex':                    require ('./js/okex.js'),
    'phemex':                  require ('./js/phemex.js'),
    'poloniex':                require ('./js/poloniex.js'),
    'ripio':                   require ('./js/ripio.js'),
    'upbit':                   require ('./js/upbit.js'),    
}

// ----------------------------------------------------------------------------

for (const exchange in exchanges) {
    const ccxtExchange = ccxt[exchange]
    const baseExchange = Object.getPrototypeOf (ccxtExchange)
    if (baseExchange === ccxt.Exchange) {
        Object.setPrototypeOf (ccxtExchange, Exchange)
        Object.setPrototypeOf (ccxtExchange.prototype, Exchange.prototype)
    }
}

module.exports = deepExtend (ccxt, {
    version,
    Exchange,
    exchanges: unique (ccxt.exchanges.concat (Object.keys (exchanges))).sort (),
}, exchanges)
