import pandas as pd
import rethinkdb as r
import datetime, sys

if len(sys.argv) != 2:
	print ("Icorrect arguments")
	exit(1)

plant = sys.argv[1]
df = pd.read_csv( plant + '.csv')
r.connect('localhost', 28015).repl()
try:
	r.db('farm').table_create(plant).run()
except:
	print ("Table already present. Updating")
	pass

print ("Starting data loading")

for index, row in df.iterrows():
    data = {
        'timestamp': int(row['timestamp']),
        'temperature': int(row['temperature']),
        'humidity': int(row['humidity']),
        'moisture': int(row['moisture']),
        'day': int(row['day'])
    }
    r.db('farm').table(plant).insert(data).run()

print ("Done data loading")


