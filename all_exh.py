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

def dg(currency):
  dg = api.getbalance(currency)
  print(dg)
  return (dg)

#https://support.bittrex.com/hc/en-us/articles/115003723911
#покупка продажа

#свершившиеся сделки
b2=getorderhistory()
p2=pl.hist(pair,cou)


#открытые сделки
def opord(bir,pair):
  if bir=='T':
    b3=api.getopenorders(pair)
    ext=b3
    
  elif bir=='P':
    p3=pl.opord(pair)
    ext=p3
  print (ext)
  return (ext)

#текушие цены
b4=api.getticker()
p4=pl.tick(par)

#все свои монеты 
b5=api.getbalances(currency)
p5=pl.a1('returnBalances')
