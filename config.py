import os
#телеграмм api ключ
tap=os.environ.get ('TELE_API')
#телеграмм личный id
tid='TELE_ID'
#db
dbname='DB_NAME'
dbuser='DB_USER'
dbhost='DB_HOST'
dbpass='DB_PASS'
#poloniex api 
pap='POLO_API'
#poloniex api key
pid='POLO_KEY'

#Общие настройки 
#количесво последних ордеров которое мы проверяем. Если долго не было активности надо проверить больше ордеров
n_ord_count=10
