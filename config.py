import os
#телеграмм api ключ
tap=os.environ.get ('TELE_API')
#телеграмм личный id
tid=os.environ.get ('TELE_ID')
#db
dbname=os.environ.get ('DB_NAME')
dbuser=os.environ.get ('DB_USER')
dbhost=os.environ.get ('DB_HOST')
dbpass=os.environ.get ('DB_PASS')
#poloniex api 
pap=os.environ.get ('POLO_API')
#poloniex api key
pid=os.environ.get ('POLO_KEY')

#Общие настройки 
#количесво последних ордеров которое мы проверяем. Если долго не было активности надо проверить больше ордеров
n_ord_count=10
