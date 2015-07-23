import requests
from pandas.io.json import json_normalize
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections
import datetime

r = requests.get('http://www.citibikenyc.com/stations/json')

key_list = [] #unique list of keys for each station listing
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)

#json_normalize is used since this comes in a different format
df = json_normalize(r.json()['stationBeanList'])

print df['totalDocks'].mean()

condition = (df['statusValue'] == 'In Service')
print df[condition]['totalDocks'].mean()

print df['totalDocks'].median()
print df[df['statusValue'] == 'In Service']['totalDocks'].median()

con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

with con:
	for station in r.json()['stationBeanList']:
		#id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
		cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids] 

#create the table
#in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

exec_time = parse(r.json()['executionTime'])

print exec_time

with con:
	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)',((exec_time-datetime.datetime(1970,1,1)).total_seconds(),))

id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

#loop through the stations in the station list
for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']

#iterate through the defaultdict to update the values in the database
with con:
    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + str((exec_time-datetime.datetime(1970,1,1)).total_seconds()) + ";")	

for i in range(60):
	r = requests.get('http://www.citibikenyc.com/stations/json')
	exec_time = parse(r.json()['executionTime'])

	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', ((exec_time-datetime.datetime(1970,1,1)).total_seconds(),))
	con.commit()

	id_bikes = collections.defaultdict(int)
	for station in r.json()['stationBeanList']:
		id_bikes[station['id']] = station['availableBikes']

	for k,v in id_bikes.iteritems():
		cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + str((exec_time-datetime.datetime(1970,1,1)).total_seconds()) + ";")
	con.commit()

	time.sleep(60)


with con:
	cur.execute('SELECT * FROM citibike_reference')
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df = pd.DataFrame(rows, columns = cols)

	cur.execute('SELECT * FROM available_bikes')
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df2 = pd.DataFrame(rows, columns = cols)

con.close()

'''df['availableBikes'].hist()
plt.show()

df['totalDocks'].hist()
plt.show()'''
'''
count1 = 0
count2 = 0
for i in range(len(df['statusValue'])):
	if df['statusValue'][i] == 'In Service':
		count1 += 1
	else:
		count2 += 1
print 'there are', count1, 'stations in service'
print 'there are', count2, 'stations not in service'

count3 = 0
for i in range(len(df['testStation'])):
	if df['testStation'][i] == True:
		count3 += 1
print 'there are', count3, 'test stations'

mean_sum = 0
count_tot = 0
for i in range(len(df['availableBikes'])):
	mean_sum += df['availableBikes'][i]
	count_tot += 1
mean = float(mean_sum) / count_tot
print 'the average number of bikes available is', mean

median_list = []
for i in range(len(df['availableBikes'])):
	median_list.append(df['availableBikes'][i])
median_list.sort()
med = median_list[len(median_list)//2]
print 'the median number of bikes availabe is', med
'''
