import sqlite3

# Connect to DB
connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()
print('Database Initialized')

def showAllUsers():
    cursor.execute("SELECT rowid, * FROM Users")
    people = cursor.fetchall()
    
    for person in people:
        print(f"{person}")

def showGroupusers():
    num = str(input("Enter group num: "))
    
    cursor.execute("SELECT * FROM Users WHERE group_num = (?)", num)
    people = cursor.fetchall()
    
    for person in people:
        print(f"{person}")

showGroupusers()
print()

# To send changes to DB
connection.commit()

# To close DB
cursor.close()
connection.close()
print('SQLite Connection closed')

