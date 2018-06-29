import requests
import json
import datetime
import sys, traceback
import config
import pl6 as pl
import all_exh as ex
import bd as bd
from time import sleep






url = 'https://api.telegram.org/bot'+str(config.tap)+':AAGRl3CVErK8dVrvvoJustYAB_Z6C8seSu4/'
global last_id #номер последней записи в чате телеги
global cou
global ord_id #номер последнего выполненного ордера 
last_id=0
ord_id=0
a=config.pap
b=config.pid

def get_updates_j():
	url1 = url+'getUpdates'
	#params = {'timeout': 100, 'offset': None}
	#print(url1)
	r = requests.get(url1)#,params)
	return r.json()
def first_all (v1):
	v2=v1['text']
	wo= v2.split()
	#print(v1['chat_id'])
	command=wo[0].lower()
	bir=command[0]
	command=command[1:10]
	dlina=len(wo)
	cm={1:'alg',
		2:'bal',
		3:'alg01',
		4:'log1',
		5:'log2',
		6:'elect',
		7:'sell',
		8:'buy',
		9:'last',
		10:'price',
	        11:'ord'
	       }
	#\r\n - перевод строки внутри сообщения
	if v1['chat_id']!=config.tid:
		rst='привет'
	elif command==cm[1]:
		if dlina!=6:
			rst=str(dlina)+'Верный формат :\r\n*alg para sum n % %'
		else:
			rst=sell1(wo)
	elif command==cm[2]:
		
		#f=pl.a1('returnBalances')
		#g=ret_bal()
		rst=pl.tick('all')
		
		#print(rst)
		#alg1(bir)
	elif command==cm[3]:
		#rst=pl.a1('returnBalances')
		alg01(bir)
	elif command==cm[4]:
		f = open("log1.txt", 'r')
		rst=f.read()
	elif command==cm[5]:
		f = open("log2.txt", 'r')
		rst=f.read()
	elif command==cm[6]:
		rst=bd.sql(v2)
	elif command==cm[7] or command==cm[8]:
		rst=cre_ord(wo,dlina,command)
	elif command==cm[9]:
		if dlina<2:
			cou=10
		else:
			try:
				cou=int(wo[1])
			except:
				send_m(config.tid,'Верный формат :\r\n*last n para')
				cou=10
				pass
		if dlina<3:
			par='all'
		else:
			par=wo[2]
			par=par.upper()
			# par='all'
		rst,g2=last1(1,par,cou,bir)
	elif command==cm[10]:
		rst=pl.ret_bal()
	elif command==cm[11]:
		rst='ок'
		ww=ex.opord(bir,'all')	
	else:
		f=str()
		for key in cm:
    			f=f+cm[key]+'\r\n'
		rst='Текущие команды:\r\n'+f+'\r\nПеред командой нужно ставить букву необходимой биржи:\r\n\P-polo,T-bittrex,N-binance,K-kucoin'
	return (rst)
def last1(typ,pair,cou,bir):
	if bir=='p':
		r0=pl.hist(pair,cou)
	elif bir=='t':
		r0=pl.hist(pair,cou)
	elif bir=='n':
		r0=pl.hist(pair,cou)
	else:
		r0=pl.hist(pair,cou)

	g=str()
	#print(r0)
	q0=json.dumps(r0)
	#print(q0)
	
	if pair !='all':
		q=q0.replace('[{','{"'+pair+'":[{')
		q=q.replace('}]','}]}')
	else:
		q=q0.replace(': [{','): [{')
		q=q.replace('"U','person("U')
		q=q.replace('"B','person("B')
	r=eval(q)

	if typ==1:
		g1=last1_1(r)
		g2=[]
	else:
		g1,g2=last1_2(r)
	return (g1,g2)
def last1_1(r):
	i=0
	g=str()
	global k
	k=0
	#print(r)
	#send_m(config.tid,r)

	for key in r.keys():

		while i<len(r[key]):
			#print(r[key][i])
			g=g+' '+str(key)+' '+r[key][i]['total']+'\r\nкол-во: '+r[key][i]['amount']+'\r\n'+r[key][i]['type']+' цена: '+r[key][i]['rate']+'\r\nord '+r[key][i]['orderNumber']+'\r\n'
			i=i+1

		i=0
		#g=g+' '+str(key)+' '+r[key][1]['total']+' '+r[key][1]['amount']+'\r\n'
		k=k+1
	return (g)
def last1_2(r):
	i=0
	g1=[]
	g2=[]
	global k
	k=0
	for key in r.keys():
		while i<len(r[key]):
			s1=r[key][i]['orderNumber']
			s2=str(key)+' '+r[key][i]['total']+'\r\nкол-во: '+r[key][i]['amount']+'\r\n'+r[key][i]['type']+' цена: '+r[key][i]['rate']+'\r\nord '+r[key][i]['orderNumber']+'\r\n'
			
			g1.append(s1)
			g2.append(s2)
			i=i+1
		i=0
		#"orderNumber"=ido
		k=k+1
	#print(g)
	return (g1,g2)
def cre_ord(wo,dlina,command):
	if dlina==1:
		rst='Верный формат :\r\n*sell valuta price btc n\r\nЕсли btc нет берем 0.00010100 btc, если 0 значит берем n(количество монет),торг к баку(u_ иначе только валюта (к бтс))'
	else:
		if dlina==3:
			nn=float(0.000101)/float(wo[2])
		elif float(wo[3])==0:
			nn=float(wo[4])
		else:
			nn=float(wo[3])/float(wo[2])
		val=wo[1]
		val0=val[0:2]
		#print(val0)
		if val0=='u_':
			val=val[2:6]
			val='USDT_'+val.upper()
			nn=round(nn,7)
		else:
			val='BTC_'+val.upper()
			nn=round(nn,3)
		price=str(wo[2])

		print(val,price,nn,command)
		if command=='sell':
			ord=pl.sell(val,price,nn)
		else:
			ord=pl.buy(val,price,nn)
		rst='ордер создан'+str(ord)
	return rst
def alg01(bir):

	o2_="select ido,idp,pair,val_sell::text,val_buy::text,amount_c::text,amount_p::text,last_type from public.alg_data where alg=1 and birja="+"'"+"polo"+"'"+" and activ=1 and ido=0"
	a=bd.sql(o2_);o2=[];i=0
	o3=[]
	while i<len(a):
		p=list(a[i])
		o3.append(p)
		i+=1
	#print(o3)
	i=0
	while i<len(o3):
		if o3[i][7]==0:
			am=rou(rou(o3[i][3])*rou(o3[i][5]))
			#print('sell',o3[i][2],	rou(o3[i][3]),rou(o3[i][5]),am)
			ord=pl.sell(o3[i][2],rou(o3[i][3]),rou(o3[i][5]))
			zd=int(ord['orderNumber'])
			o3[i][0]=zd
			o3[i][6]=am

		else:
			f=2
			am=rou(rou(o3[i][6])/rou(o3[i][4]))
			#print('buy',o3[i][2],rou(o3[i][4]),am)
			ord=pl.buy(o3[i][2],rou(o3[i][4]),am)
			print(ord)
			ido=int(ord['orderNumber'])
			o3[i][0]=ido
			o3[i][5]=am

			# заменяем ido,amount_c(am) на новое
		i=i+1
		#берем ido и остальное и обновляем запись в alg_data
	#print(o3)
	i=0
	while i<len(o3):
		u1='update public.alg_data set ido={} ,dt_last=current_date where idp={};commit;'.format(o3[i][0],o3[i][1])
		i=i+1
		print(u1)
		dat=bd.sql(u1)
	#dat=bd.sql(u1)
	return ('ok')
	#повтор
def re_arg01(bir):
	return (bir)
def trade_ntf(n1,n2):
	#создать новою переменную
	#при доавление биржы переменную нужно перобразовать в массив
	global ord_id
	#print(ord_id)
	#print(type(n1))
	#print(n1)
	if ord_id!=n1[0]:
		if ord_id==0:
			ord_id=n1[0]
		else:
			#узнаем сколько заявок до ord_id
			f1=n1.index(ord_id)
			#срез до ord_id
			n2=n2[:f1]
			ord_id=n1[0]
			i=0
			y=str()
			while i<len(n2):
				y=y+str(n2[i])
				i+=1
			send_m(config.tid,'trade'+y)

		
	return (n1)

def pre_alg(bir):
	#берем id n-последнии свершихся сделок
	n1,n2=last1(2,'all',config.n_ord_count,bir)
	
	re=alg1(bir,n1)
	if len(n1)!=0:
		f=trade_ntf(n1,n2) 
	try:
		
		pass
	except:
		pass
	return re

def alg1(bir,n1):
	o1=n1
	o2_="select ido,idp,pair,val_sell::text,val_buy::text,amount_c::text,amount_p::text,last_type from public.alg_data where alg=1 and birja="+"'"+"polo"+"'"+" and activ=1 and ido!=0"
	a=bd.sql(o2_);dat=a;o2=[];i=0
	while i<len(a):
		c=str(a[i][0])
		o2.append(c)
		i=i+1
	a = set(o1);b = set(o2)
	#свершившиеся ордера
	c=a&b;o3=[];i=0;с=list(c)
	for i0 in c:
		i=0
		i0=int(i0)
		while i<len(dat):
			if i0==dat[i][0]:
			#	print('ок')
				y=list(dat[i])
				o3.append(y)
			i+=1
	print(o3)
	#разобраться с комимсиями и где что умножать что бы получить исодное значение в бтс(родителе)
	#ставим новый обратный ордер на основе о3
	#dat=.replace('Decimal(','')
	#dat=dat.replace(')','')
	i=0
	while i<len(o3):
	#last_type
		if o3[i][7]==1:
			f=1
			
			qq=float (pl.tick(o3[i][2]))
			if qq >rou(o3[i][3]):
				price=rou(qq)
			else:
				price=rou(o3[i][3])
			am=rou(rou(o3[i][5])*price)
			#print('sell',o3[i][2],	rou(o3[i][3]),rou(o3[i][5]),am)
			ord=pl.sell(o3[i][2],price,rou(o3[i][5]))
			ido=int(ord['orderNumber'])
			o3[i][0]=ido
			o3[i][6]=am
			o3[i][7]=0
			# заменяем ido,amount_p на новое
		else:
			f=2
			qq=float (pl.tick(o3[i][2]))
			if qq <rou(o3[i][4]):
				price=rou(qq-(qq*0.01))
				#на один процента меньше текущей цены
			else:
				price=rou(o3[i][4])
			am=rou(rou(o3[i][6])/price)
			print('buy',o3[i][2],price,am)
			ord=pl.buy(o3[i][2],price,am)
			print(ord)
			ido=int(ord['orderNumber'])
			o3[i][0]=ido
			o3[i][5]=am
			o3[i][7]=1
		i=i+1
		#берем ido и остальное и обновляем запись в alg_data
	i=0
	while i<len(o3):
		u1='update public.alg_data set ido={},amount_c={},amount_p={},last_type={},circle=case when last_type=1 then circle+1 else circle  end ,dt_last=current_date where idp={};commit;'.format(o3[i][0],o3[i][5],o3[i][6],o3[i][7],o3[i][1])
		i+=1
		print(u1)
		dat=bd.sql(u1)
	if len(c)>0:
		send_m(config.tid,'trade в alg1')
	return ('ok')
	#повтор
	
def alg02():
	#пампадампа включение/отключение/перезапуск(с учетем процента) монеты 
	
	return ('ok')	
	
def alg2():
	#пампадампа
	
	return ('ok')

def sell0(wo):
	n1= float (wo[2])
	n2= int (wo[3])
	n3= int (wo[4])
	para=wo[1]
	a=[]
	for i in range(n2):
		n1=round(n1+n1*n3*0.01,8)
		n4='@'+para+'@'+str(n1)+'@'
		a.append(n4)
	with open("ff.txt", "w") as file:
		print(*a, file=file, sep="\n")
	#print(m_txt)
	return (a)
def sell1(wo):
	n1= float (wo[2])
	n2= int (wo[3])
	n3= float (wo[4])
	n4= float (wo[5])
	para=wo[1].upper()
	a=[]
	qq=float (pl.tick(para))
	for i in range(n2):
		n1=round(n1+n1*n3*0.01,8)
		#генерацая относительно текушей цены
		if n1>qq:
			qq1=0
		else:
			qq1=1
		qq1=str(qq1)
		nn1=str(n1)
		nn2=nn1.replace(',','.')
		n5="insert into public.alg_data (idp,ido,pair,val_sell,val_buy,amount_c,amount_p,last_type,circle,alg,dt_open,activ,birja) VALUES (nextval("+"'"+"public.seq_alg_data"+"'"+"),0,'"+para+"',"+nn2+",0.000001,5,0.000101,"+qq1+",0,1,current_date,1,"+"'"+"polo"+"'"+");commit;"


		dat=bd.sql(n5)
	n6="update public.alg_data set amount_c=amount_p/val_sell,val_buy=val_sell-(val_sell*0.0"+str(n4)+") where pair='"+para+"' and alg=1 and dt_last is null;commit;"
	print(n6)
	dat=bd.sql(n6)
	a='ок'
	return (a)
def get_mes():
	data=get_updates_j()
	
	if data['ok']==True:
		#print(data)
		if len(data['result'])>0:
			m_id=data['result'][-1]['message']['chat']['id']
			m_txt=data['result'][-1]['message']['text']
			m_upd=data['result'][-1]['update_id']
			global last_id
			if last_id!=m_upd:
				last_id=m_upd
				ms = {'chat_id': m_id, 'text': m_txt ,'upd_id':m_upd}
				return ms
	return None
def send_m (chat_id,text='wait'):
	url1=url+'sendmessage?chat_id={}&text={}'.format(chat_id,text)
	requests.get(url1)
class person(object):
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return self.name

	def __repr__(self):
		return "'"+self.name+"'"
def rou(a):
	return(	round(float(a),8))
def main():
	#get_mes()
	u=0
	#r=pl.sell('BTC_XEM',0.00003380,3) 54310439308 [1] ido
	#print(r)
	while True:
		ans=get_mes()
		t=0
		if ans !=None:
			chat_id=ans['chat_id']
			s1=first_all(ans)
			send_m(chat_id,s1)
			now = datetime.datetime.now()
			#print(now)
		#elif Key!=0:
		elif t==1:
			chat_id=ans['chat_id']
			s1=first_all(ans)
			send_m(chat_id,s1)
			now = datetime.datetime.now()
			#print(now)
		#else:
		#	continue
		u=u+5 #примерный подсчет времени по циклу

		if u==60:
			pre_alg('p')

			#alg1()
			#dat=bd.sql('SELECT * FROM public.alg_data LIMIT 3')
			u=0
		#else:
		#	continue

		sleep(5)



if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		var = traceback.format_exc()
		send_m(config.tid,var)
		with open("log1.txt", "a") as file:
			print(var, file=file, sep="\n")
		with open("log2.txt", "w") as file:
			print(var, file=file, sep="\n")
		raise
