import psycopg2
import psycopg2.extras
import config as c

def sql(sql):
	try:
		conn = psycopg2.connect("dbname='"+c.dbname"' user='"+c.dbuser"'"
								" host='"+c.dbhost"' password='"+c.dbpass"'")
	except psycopg2.Error as err:
		print("Connection error: {}".format(err))
	try:
		if sql[0:3]=='sel':
			cur = conn.cursor()
			cur.execute(sql)
			data = cur.fetchall()
		else:
			cur = conn.cursor()
			cur.execute(sql)
			data='ok'
	except psycopg2.Error as err:
		print("Query error: {}".format(err))
	return (data)

#sq = "selECT * FROM public.alg_data LIMIT 3"
#r=sql(sq)
#print(r)
