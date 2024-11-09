import sqlite3

# Connect to DB
connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()
print('Database Initialized')

def show_Users():
    cursor.execute("SELECT rowid, * FROM Users")
    people = cursor.fetchall()
    
    for person in people:
        print(f"{person}")

show_Users()
# To send changes to DB
connection.commit()

# To close DB
cursor.close()
connection.close()
print('SQLite Connection closed')

