import requests
import sqlite3 as lite
import datetime
import pandas as pd

my_api_key = '7083a221636c7d58dda25f80cdf9d7b1'
my_api_url = 'https://api.forecast.io/forecast/' + my_api_key
# dictionary of 5 cities with lat/lons
cities = {  "Atlanta": '33.762909,-84.422675',
			"Denver": '39.761850,-104.881105',
			"Miami": '25.775163,-80.208615',
			"Nashville": '36.171800,-86.785002',
			"Seattle": '47.620499,-122.350876' 
		}

# set the time for "now" - the time the code is executed
# this makes the reference time the same for all queries
now = datetime.datetime.now()

# set up the db
con = lite.connect('weather_api.db')
cur = con.cursor()
# set up the tables
with con:
	cur.execute('DROP TABLE IF EXISTS temp')
	cur.execute('CREATE TABLE IF NOT EXISTS temp ( day_recorded INT, Atlanta REAL, Denver REAL, Miami REAL, Nashville REAL, Seattle REAL )')

# we go back 30 days, and start iterating daily from there
# day_of_query starts 30 days in the past (from now)
day_of_query = now - datetime.timedelta(days=30)
# fill in the days
with con:
	while day_of_query < now:
		cur.execute("INSERT INTO temp ( day_recorded ) VALUES (?)", (int(day_of_query.strftime("%Y%m%d%H%M%S")),))
		day_of_query += datetime.timedelta(days=1)

# loop through the cities we've chosen and get data
# using the api
for k,v in cities.iteritems():
	# start the query at 30 days ago for each city
	day_of_query = now - datetime.timedelta(days=30)
	while day_of_query < now:
		# tack onto my_api_url the lat/lon pairs and the query day
		r = requests.get(my_api_url + '/' + v + ',' + day_of_query.strftime("%Y-%m-%dT%H:%M:%S"))
		# set the REAL value for each city to the max temperature on the query day
		with con:
			x = int(day_of_query.strftime("%Y%m%d%H%M%S"))
			cur.execute('UPDATE temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_recorded = ' + str(x) + ';')
		# increment the query date by 1 day
		day_of_query += datetime.timedelta(days=1)
# close the connection to the db

df = pd.read_sql_query("SELECT * FROM temp ORDER BY day_recorded", con)

con.close()



'''
import datetime
import requests
import sqlite3 as lite
import pandas as pd

cities = {"Atlanta":'33.762909,-84.422675',
		'Austin': '30.303936,-97.754355',
		'Boston': '42.331960,-71.020173',
		'Chicago': '41.837551,-87.681844',
		'Cleveland':'41.478462,-81.679435'
		}

city_list = cities.keys()
city_list = [str(x) + ' TEXT' for x in city_list]

con = lite.connect('weather.db')
cur = con.cursor()

url = 'https://api.forecast.io/forecast/7083a221636c7d58dda25f80cdf9d7b1/'

with con:
	cur.execute('DROP TABLE IF EXISTS max_temps')
	cur.execute('CREATE TABLE max_temps (period TEXT, Atlanta REAL, Austin REAL, Boston REAL, Chicago REAL, Cleveland REAL ) ')

end_date = datetime.datetime.now()

query_date = end_date - datetime.timedelta(days=30)

with con:
	while query_date < end_date:
		cur.execute('INSERT INTO max_temps (period) VALUES (?)',(query_date.strftime("%Y-%m-%dT%H:%M:%S"),))
		query_date += datetime.timedelta(days=1)

df = pd.read_sql_query("SELECT * FROM max_temps ORDER BY period", con, index_col = 'period')
print df.columns.values

for k, v in cities.iteritems():
	query_date = end_date - datetime.timedelta(days=30)
	while query_date < end_date:
		r = requests.get(url + v + "," + query_date.strftime("%Y-%m-%dT%H:%M:%S"))
		with con:
			cur.execute('UPDATE max_temps SET ' + str(k) + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE period = ' + query_date.strftime("%Y-%m-%dT%H:%M:%S"))
		query_date += datetime.timedelta(days = 1)


df = pd.read_sql_query("SELECT * FROM max_temps ORDER BY period", con, index_col = 'period')

#close database upon completion
con.close()

'''

'''for k, v in cities:
	r = requests.get('https://api.forecast.io/forecast/7083a221636c7d58dda25f80cdf9d7b1/' + cities[k] + "," + t_t))




with con:
	cur.execute('UPDATE max_temps SET ')

start_date = datetime.datetime.now() - datetime.timedelta(days = 30)
'''

''''print r.json()'''
'''t_t = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")'''
#df = pd.read_sql_query("SELECt * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')


'''r = requests.get('https://api.forecast.io/forecast/7083a221636c7d58dda25f80cdf9d7b1/33.762909,-84.422675,' + t_t)'''
'''
#this returns the daily max temperature
weathertest.r.json()['daily']['data'][0]['temperatureMax']

https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME


https://api.forecast.io/forecast/7083a221636c7d58dda25f80cdf9d7b1/33.762909,-84.422675,2015-07-23T18:34:19
'''
