import sqlite3
try:
    connection = sqlite3.connect('Database for Expense tracker.db')
    cursor = connection.cursor()
    print('Database Initialized')

    query = 'select sqlite_version();'
    cursor.execute(query)

    result = cursor.fetchall()
    print('SQLite version is {}'.format(result))

    cursor.close()
    
except sqlite3.Error as error:
    print('Error occured - ', error)
    
finally:
   
    if connection:
        connection.close()
        print('SQLite Connection closed')

