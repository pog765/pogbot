from urllib.parse import urlencode
import urllib.request
import json
import time
import hmac
import hashlib
import config


key =btap
secret =btid
public = ['getmarkets', 'getcurrencies', 'getticker', 'getmarketsummaries', 'getmarketsummary', 'getorderbook', 'getmarkethistory']
market = ['buylimit', 'buymarket', 'selllimit', 'sellmarket', 'cancel', 'getopenorders']
account = ['getbalances', 'getbalance', 'getdepositaddress', 'withdraw', 'getorder', 'getorderhistory', 'getwithdrawalhistory', 'getdeposithistory']


def query( method, values={}):
    if method in public:
        url = 'https://bittrex.com/api/v1.1/public/'
    elif method in market:
        url = 'https://bittrex.com/api/v1.1/market/'
    elif method in account:
        url = 'https://bittrex.com/api/v1.1/account/'
    else:
        return 'Something went wrong, sorry.'

    url += method + '?' + urlencode(values)

    if method not in public:
        url += '&apikey=' + key
        url += '&nonce=' + str(int(time.time()))
        #url=url.encode()
        signature = hmac.new(secret.encode(), url, hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
    else:
        headers = {}

    req = urllib.request.Request(url, headers=headers)
    response = json.loads(urllib.request.urlopen(req).read())
    print(response)
    if response["result"]:
        return response["result"]
    else:
        return response["message"]


def getmarkets():
    return query('getmarkets')



def getcurrencies():
    return query('getcurrencies')

def getticker( market):
    return query('getticker', {'market': market})

def getmarketsummaries():
    return query('getmarketsummaries')

def getmarketsummary( market):
    return query('getmarketsummary', {'market': market})

def getorderbook( market, type, depth=20):
    return query('getorderbook', {'market': market, 'type': type, 'depth': depth})

    def getmarkethistory( market, count=20):
        return query('getmarkethistory', {'market': market, 'count': count})

    def buylimit( market, quantity, rate):
        return query('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def buymarket( market, quantity):
        return query('buymarket', {'market': market, 'quantity': quantity})

    def selllimit( market, quantity, rate):
        return query('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def sellmarket( market, quantity):
        return query('sellmarket', {'market': market, 'quantity': quantity})

    def cancel( uuid):
        return query('cancel', {'uuid': uuid})

    def getopenorders( market):
        return query('getopenorders', {'market': market})

def getbalances():
    return query('getbalances')

    def getbalance( currency):
        return query('getbalance', {'currency': currency})

    def getdepositaddress( currency):
        return query('getdepositaddress', {'currency': currency})

    def withdraw( currency, quantity, address):
        return query('withdraw', {'currency': currency, 'quantity': quantity, 'address': address})

    def getorder( uuid):
        return query('getorder', {'uuid': uuid})

    def getorderhistory( market, count):
        return query('getorderhistory', {'market': market, 'count': count})

    def getwithdrawalhistory( currency, count):
        return query('getwithdrawalhistory', {'currency': currency, 'count': count})

    def getdeposithistory( currency, count):
        return query('getdeposithistory', {'currency': currency, 'count': count})

#print(getmarkets())
print(getticker('BTC-GLD'))
print(getbalances())
