import urllib.parse,  urllib.request
import json, hashlib, hmac, time, requests
import config
from datetime import datetime, timedelta,date

def a1(cmdp,req={}):
	api= 'https://poloniex.com/tradingApi'
	key=config.pap
	secret=config.pid
	if cmdp=='hist':
		cmdp="returnTradeHistory&currencyPair=all&limit=10"
	data1 = {'command': cmdp,
			 'nonce'  : int(time.time() * 1000)
	}
	#data = urllib.parse.urlencode(data).encode()
	req['command'] = cmdp
	req['nonce'] = int(time.time()*2000) # было 1000, паоменял в надежде убрать баг heroku  по таймауту
	data = urllib.parse.urlencode(req).encode()
	signature = hmac.new(secret.encode(), data, hashlib.sha512)
	headers = {'Key' : key,
			   'Sign': signature.hexdigest(),
			   'Content-Type': 'application/x-www-form-urlencoded'
			  }
	request = urllib.request.Request(url=api, data=data, headers=headers, method='POST')
	#ret = urllib.request.urlopen(request).read().decode()
	
	#ret = requests.post('https://poloniex.com/tradingApi', data=data, headers=headers)
	#rr=json.loads(ret.text)
	#print(rr)
	try:
		ret = requests.post('https://poloniex.com/tradingApi', data=data, headers=headers)
		rr=json.loads(ret.text)
	except Exception:
		rr={}
		#{'BTC_Z': [{'globalTradeID': 379522526}]}
		
	return rr

def hist(currencyPair,limit):
	a2=a1('returnTradeHistory',{"currencyPair":currencyPair,"start":10000,"limit":limit})
	return a2

def opord(currencyPair):
	a2=a1('returnOpenOrders',{"currencyPair":currencyPair})
	return a2

def buy(currency_pair, rate, amount):
	a3=a1('buy', {"currencyPair": currency_pair, "rate": rate, "amount": amount})
	return a3


def sell( currency_pair, rate, amount):
	a4=a1('sell', {"currencyPair": currency_pair, "rate": rate, "amount": amount})
	return a4

def tick(par):
	ee=requests.get('https://poloniex.com/public?command=returnTicker')
	r0=json.loads(ee.text)
	if par=='all': 
		r1=r0
	else:
		r1=r0[par]['last']
	return(r1)

def ret_bal():
	f=a1('returnBalances')
	f1=tick('all')
	us=['BTC'] # что показываем в паре к баксу
	a3=str()
	for key in f.keys():
		if float(f[key])>0:
			if key=='BTC':
				pair='USDT_'+key.upper()
			else:
				pair='BTC_'+key.upper()
			for key1 in f1.keys():
				if key1==pair:
					pr=round(float(f1[key1]['percentChange'])*100,2)
					a3=a3+key1+' ls:'+f1[key1]['last'] + '\r\n'+'% 24:'+str(pr) + '\r\n'+'/ 24:'+f1[key1]['high24hr'] + '\r\n'+'\ 24:'+f1[key1]['low24hr'] + '\r\n'
	return a3

