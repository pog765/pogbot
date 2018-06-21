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
	#rr=json.loads(text)#['LTC']
	#with open("ff.txt", "w") as file:
	#    print(*rr, file=file, sep="\n")
	#rr=json.loads(ret.read())
	#print(ret)
	try:
		rr=json.loads(ret.text)
	except json.JsonDecodeError as error:
		if (error.msg.startswith("Expecting") and error.pos == 0):
			pass
		else:
			raise
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
	print(rr)
	return(rr)
