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
	
	ret = requests.post('https://poloniex.com/tradingApi', data=data, headers=headers)
	rr=json.loads(ret.text)
	print(rr)
	#try:
	#	ret = requests.post('https://poloniex.com/tradingApi', data=data, headers=headers)
	#	rr=json.loads(ret.text)
	#except Exception:
	#	rr={}
		#{'BTC_Z': [{'globalTradeID': 379522526}]}
		
	return rr

def hist(currencyPair,limit):
	a2=a1('returnTradeHistory',{"currencyPair":currencyPair,"start":10000,"limit":limit})
	return a2

def buy(currency_pair, rate, amount):
	a3=a1('buy', {"currencyPair": currency_pair, "rate": rate, "amount": amount})
	return a3


def sell( currency_pair, rate, amount):
	a4=a1('sell', {"currencyPair": currency_pair, "rate": rate, "amount": amount})
	return a4

def tick(par):
	ee=requests.get('https://poloniex.com/public?command=returnTicker')
	rr=json.loads(ee.text)
	rr=rr[par]['last']
	#print(rr)
	return(rr)

def ret_bal():
	a2=a1('returnBalances')
	us=['BTC'] # что показываем в паре к баксу
	a3=str()
	#for key in a2.keys():
		#if key=='BTC':
			#key='USDT_'+val.upper()
		##elif key in us:
		#else:
			#key='BTC_'+val.upper()
		#a3=a3+key+' '+str(tick(key)) + '\r\n'
		
	return a3

