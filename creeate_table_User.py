import sqlite3
conn = sqlite3.connect('timeEvent.db')
print "Opened database successfully"
conn.execute('CREATE TABLE Users (name TEXT, password TEXT, email TEXT, extra TEXT)')
print "Table created successfully"
conn.close()