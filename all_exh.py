from bit1 import bittrex as bit
import pl6 as pl
import config as cf
import json

# Get these from https://bittrex.com/Account/ManageApiKey
api = bit(cf.bitap, cf.bitid)

# Market to trade at
trade = 'BTC'
currency = 'BSD'
bit_market = '{0}-{1}'.format(trade, currency)
pl_market = '{0}_{1}'.format(trade, currency)
# Amount of coins to buy
amount = 100
# How big of a profit you want to make
multiplier = 1.1

def dg(currency):
  dg = api.getbalance(currency)
  print(dg)
  return (dg)

#https://support.bittrex.com/hc/en-us/articles/115003723911
#для каждой бирже общий преобрадователь входных(0),выходных(1) данных 
def pl_transform(a,v):
    if v==0:
        b=a
    else:
        b=a
    return b

def bit_transform(a0,v):
    if v==0:
        b=a0

    else:
        for a in a0:
            print(type(a))
            a['orderNumber']=a.pop('OrderUuid')
            a['pair'] = a.pop('Exchange').replace('BTC-','BTC_').replace('USDT-','USDT_')
            a['total']=str(a.pop('Price'))
            a['amount'] = str(a.pop('Quantity'))
            a['type'] = a.pop('OrderType').replace('LIMIT_BUY','buy').replace('LIMIT_SELL','sell')
            a['rate']=str(e_form(a.pop('PricePerUnit')))

        b=a0

    return b
#покупка продажа

#свершившиеся сделки
def hist0(pair,cou):
    b2=bit_transform(api.getorderhistory(pair,cou),1)
    p2=pl.hist(pair,cou)
    ext=0
    g=[]
    for key in p2.keys():
        for i in p2[key]:
            i['pair']=key
            g.append(i)
        #print(p2[key][i]["globalTradeID"])
    #sorted(d.items(), key=lambda x: x[1])
    g=sorted(g,key= lambda d: d['globalTradeID'], reverse=True)
    p2=pl_transform(g,1)
    js_wr(b2,'b_h.json')
    js_wr(p2,'p_h.json')
    return ext

def hist(bir,pair,cou):
    if bir=='t':
        ext=bit_transform(api.getorderhistory(pair,cou),1)
    elif bir=='p':
        p2=pl.hist(pair,cou)
        g=[]
        for key in p2.keys():
            for i in p2[key]:
                i['pair']=key
                g.append(i)
        g=sorted(g,key= lambda d: d['globalTradeID'], reverse=True)
        ext=pl_transform(g,1)
    return ext

#открытые сделки
def opord(bir,pair):
  if bir=='t':
    b3=api.getopenorders(pair)
    ext=bit_transform(b3)
    
  elif bir=='p':
    p3=pl.opord(pair)
    ext=pl_transform(p3)
  print (ext)
  return (ext)

#текушие цены
def tick(pair):
  b4=api.getticker()
  p4=pl.tick(pair)
  ext=0
  return ext

#все свои монеты
def bal():
  b5=api.getbalances(currency)
  p5=pl.a1('returnBalances')
  ext=0
  return ext

def js_wr(data,file):
    with open(file,'w') as f:
        json.dump(data,f,indent=2)

def e_form(a):
    return "%.8f" % (a)

#hist('p','all',10)
