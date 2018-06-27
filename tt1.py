from pl8 import bittrex

# Get these from https://bittrex.com/Account/ManageApiKey
api = bittrex(api, key)

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
