import pandas as pd
import sqlite3 as lite
import collections
import datetime
import matplotlib.pyplot as plt

con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query("SELECt * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
	station_vals = df[col].tolist()
	station_id = col[1:]
	station_change = 0
	for k,v in enumerate(station_vals):
		if k < len(station_vals) - 1:
			station_change += abs(station_vals[k] - station_vals[k+1])
	hour_change[int(station_id)] = station_change

def keywithmaxval(d):
	#create a list of the dict's keys and values;
	v = list(d.values())
	k = list(d.keys())

	#return the key with the max values
	return k[v.index(max(v))]

#assign the max key to max_station
max_station = keywithmaxval(hour_change)

#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[max_station ]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

plt.bar(hour_change.keys(),hour_change.values())
plt.show()