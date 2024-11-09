import sqlite3

connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()
print('Database Initialized')

cursor.execute("INSERT INTO Users VALUES('1','rizeta5','password')")
cursor.execute("INSERT INTO Users VALUES('2','dbejar','Kirby19')")
print(cursor.fetchall)
cursor.close()
connection.close()
print('SQLite Connection closed')

