from bit1 import bittrex as bit
import pl6 as pl
import config as cf

# Get these from https://bittrex.com/Account/ManageApiKey
api = bit(cf.bitap, cf.bitid)

# Market to trade at
trade = 'BTC'
currency = 'BSD'
market = '{0}-{1}'.format(trade, currency)
# Amount of coins to buy
amount = 100
# How big of a profit you want to make
multiplier = 1.1


dg = api.getbalance(currency)
print(dg)
