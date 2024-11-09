import sqlite3

connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()
print('Database Initialized')


connection.commit()

cursor.close()
connection.close()
print('SQLite Connection closed')

