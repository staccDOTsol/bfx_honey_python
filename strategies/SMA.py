import asyncio
from hfstrategy import Strategy
from bfxhfindicators import SMA as bfxSMA
from hfstrategy import Executor

class SMA ( object ):
    def __init__( self, symbol ):
        self.strategy = Strategy(
            symbol=symbol,
            indicators={
            'smaL': bfxSMA(100),
            'smaS': bfxSMA(50)
            },
            exchange_type=Strategy.ExchangeType.EXCHANGE,
            logLevel='DEBUG'
        )
        self.symbol = symbol

        @self.strategy.on_enter
        async def enter(update):
          smaS = self.strategy.get_indicators()['smaS']
          smaL = self.strategy.get_indicators()['smaL']
          if smaS.crossed(smaL.v()):
            if smaS.v() > smaL.v():
              await self.strategy.open_long_position_market(mtsCreate=update.mts, amount=1)
            else:
              await self.strategy.open_short_position_market(mtsCreate=update.mts, amount=1)
        @self.strategy.on_update_short
        async def update_short(update, position):
          smaS = self.strategy.get_indicators()['smaS']
          smaL = self.strategy.get_indicators()['smaL']
          if smaS.v() > smaL.v():
            await self.strategy.close_position_market(mtsCreate=update.mts)

        @self.strategy.on_update_long
        async def update_long(update, position):
          smaS = self.strategy.get_indicators()['smaS']
          smaL = self.strategy.get_indicators()['smaL']
          if smaS.v() < smaL.v():
            await self.strategy.close_position_market(mtsCreate=update.mts)
        

    def run ( self ):
        exe = Executor(self.strategy,  timeframe='1hr')

        exe.offline(file=self.symbol.replace('/','') + '.json')
        #print(dir(exe))
        #exe.backtest_live()
    