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

def getHighestGroup():
    cursor.execute("SELECT * FROM Users ORDER BY group_num DESC")
    highGroupNum = cursor.fetchone()[3]
    return highGroupNum

def getHighestUserID():
    cursor.execute("SELECT * FROM Users ORDER BY user_id DESC")
    highUserID = cursor.fetchone()[0]
    return highUserID

def createNewGroup():
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    groupNum = getHighestGroup() + 1
    userID = getHighestUserID() + 1
    cursor.execute("INSERT INTO Users VALUES (?,?,?,?)", (userID , user, password, groupNum))
    
    
    
    
createNewGroup()  
print()
showGroupusers()


# To send changes to DB
connection.commit()

# To close DB
cursor.close()
connection.close()
print('SQLite Connection closed')

