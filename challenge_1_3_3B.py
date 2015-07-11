import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')

cities = (('New York City','NY'),
	('Boston','MA'),
	('Chicago','IL'),
	('Miami','FL'),
	('Dallas','TX'),
	('Seattle','WA'),
	('Portland','OR'),
	('San Francisco','CA'),
	('Los Angeles','CA'))

weather = (('New York City',2013,'July','January',62),
	('Boston',2013,'July','January',59),
	('Chicago',2013,'July','January',59),
	('Miami',2013,'August','January',84),
	('Dallas',2013,'July','January',77),
	('Seattle',2013,'July','January',61),
	('Portland',2013,'July','December',63),
	('San Francisco',2013,'September','December',64),
	('Los Angeles',2013,'September','December',75))

mnth = raw_input("Please enter a month: ")
good_mnth = False

mnth_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

while good_mnth == False:
	if mnth in mnth_list:
		good_mnth = True
	else:
		mnth = raw_input("Please re-enter month correctly: ")

with con:

	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS cities')
	cur.execute('DROP TABLE IF EXISTS weather')

	cur.execute('CREATE TABLE cities (name text, state text)')
	cur.execute('CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)')

	cur.executemany('INSERT INTO cities VALUES (?,?)',cities)
	cur.executemany('INSERT INTO weather VALUES (?,?,?,?,?)',weather)

	cur.execute('SELECT * FROM cities INNER JOIN weather ON cities.name = weather.city WHERE warm_month = "%s"' % (mnth))

	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df = pd.DataFrame(rows, columns = cols)

	if len(rows) > 1:
		print 'The cities that are warmest in July are:',
		for i in range(len(rows) - 1):
			print str(df['name'][i]) + ', ' + str(df['state'][i]) + ',',
		print 'and ' + str(df['name'][len(rows)-1]) + ', ' + str(df['state'][len(rows)-1]) + '.'
	elif len(rows) == 1:
		print 'The city that is warmest in July is ' + mnth + '.'
	else:
		print 'There are no citie in the database where the warmest month is ' + mnth + '.'