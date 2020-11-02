import asyncio
from hfstrategy import Strategy
from bfxhfindicators import EMA as bfxEMA
from hfstrategy import Executor

class EMA ( object ):
	def __init__( self, symbol ):
		self.strategy = Strategy(
			symbol=symbol,
			indicators={
			'emaL': bfxEMA(100),
			'emaS': bfxEMA(20)
			},
			exchange_type=Strategy.ExchangeType.EXCHANGE,
			logLevel='DEBUG'
		)

		@self.strategy.on_enter
		async def enter(update):
		  emaS = self.strategy.get_indicators()['emaS']
		  emaL = self.strategy.get_indicators()['emaL']
		  if emaS.crossed(emaL.v()):
		    if emaS.v() > emaL.v():
		      await self.strategy.open_long_position_market(mtsCreate=update.mts, amount=1)
		    else:
		      await self.strategy.open_short_position_market(mtsCreate=update.mts, amount=1)
		@self.strategy.on_update_short
		async def update_short(update, position):
		  emaS = self.strategy.get_indicators()['emaS']
		  emaL = self.strategy.get_indicators()['emaL']
		  if emaS.v() > emaL.v():
		    await self.strategy.close_position_market(mtsCreate=update.mts)

		@self.strategy.on_update_long
		async def update_long(update, position):
		  emaS = self.strategy.get_indicators()['emaS']
		  emaL = self.strategy.get_indicators()['emaL']
		  if emaS.v() < emaL.v():
		    await self.strategy.close_position_market(mtsCreate=update.mts)
		

	def run ( self ):
		exe = Executor(self.strategy,  timeframe='1hr')

		exe.offline(file='BTCUSD.json')
		#print(dir(exe))
		#exe.backtest_live()
	