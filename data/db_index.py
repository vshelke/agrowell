import pandas as pd
import rethinkdb as r
import datetime, sys

if len(sys.argv) != 2:
	print ("Icorrect arguments")
	exit(1)
plant = sys.argv[1]
conn = r.connect('localhost', 28015).repl()
data = r.db('farm').table(plant).index_create('timestamp').run(conn)
print ("Indexing started")
print (data)



