import pandas as pd
import sqlite3 as lite
import collections
import matplotlib.pyplot as plt

con = lite.connect('weather_api.db')
cur = con.cursor()

df = pd.read_sql_query('SELECT * FROM temp ORDER BY day_recorded', con)

city_list = list(df.columns.values[1:])

for i in city_list:
	maxday = max(df[i])
	minday = min(df[i])
	meanday = df[i].mean()
	rangeday = maxday - minday
	stdday = df[i].std()
	print "For " + str(i) + ", the max is " + str(maxday) + ", the min is " + str(minday) + \
		", the range is " + str(rangeday) + ', and the mean is ' + str(meanday) +  \
		". The standard deviation is " + str(stdday)


month_change = collections.defaultdict(int)
for i in city_list:
	temp_vals = df[i].tolist()
	temp_change = 0
	for k,v in enumerate(temp_vals):
		if k < len(temp_vals) - 1:
			temp_change += abs(temp_vals[k] - temp_vals[k + 1])
	month_change[i] = int(temp_change)

def keywithmaxval(d):
	v = list(d.values())
	k = list(d.keys())
	return k[v.index(max(v))]

max_city = keywithmaxval(month_change)

print "the active max temperature of the five cities is", max_city, ". It had a total daily change in max temp over the past month of", month_change[max_city]

print month_change
