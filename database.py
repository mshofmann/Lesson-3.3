import sqlite3 as lite
import pandas as pd


citiesdump = (('New_York_City', 'NY'),
	('Boston', 'MA'),
	('Chicago', 'IL'),
	('Miami', 'FL'),
	('Dallas', 'TX'),
	('Seattle', 'WA'),
	('Portland', 'OR'),
	('San_Francisco', 'CA'),
	('Los_Angeles', 'CA'),
	('Washington', 'DC'),
	('Houston', 'TX'))
weatherdump = (('New_York_City', 2013, 'July', 'January', 62),
	('Boston', 2013, 'July', 'January', 59),
	('Chicago', 2013, 'July', 'January', 59),
	('Miami', 2013, 'August', 'January', 84),
	('Dallas', 2013, 'July', 'January', 77),
	('Seattle', 2013, 'July', 'January', 61),
	('Portland', 2013, 'July', 'December', 63),
	('San_Francisco', 2013, 'September', 'December', 64),
	('Los_Angeles', 2013, 'September', 'December', 75),
	('Washington', 2013, 'July', 'January', 63),
	('Houston', 2013, 'July', 'January', 78))
con = lite.connect('getting_started.db')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS cities2')
	cur.execute('DROP TABLE IF EXISTS weather2')
	cur.execute('create TABLE cities2 (name text, state text)')
	cur.executemany('insert into cities2 values(?, ?)', citiesdump)
	cur.execute('create TABLE weather2 (city text, year integer,' 
		'warm_month text, cold_month text, average_high integer)')
	cur.executemany('insert into weather2 values(?, ?, ?, ?, ?)', weatherdump)
	cur.execute("""select name, state, warm_month
		from cities2 
		inner join weather2 on name = city
		where warm_month = 'July'
		""")
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df = pd.DataFrame(rows, columns = cols)
citieslist = df["name"].tolist()
stateslist = df["state"].tolist()
result = (zip(citieslist, stateslist))
result = [x for i in result for x in i]
print 'The cities that are warmest in July are: ' + ', '.join(result) + '.'

