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
    
def joinGroup():
    groupNum = input("Enter the number of the group you wish to join: ")
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    userID = getHighestUserID() + 1
    cursor.execute("INSERT INTO Users VALUES (?,?,?,?)", (userID , user, password, groupNum))

def splitPurchase():
    num = str(input("Enter group num: "))
    purchase_amount = float(input("Enter total purchase amount: "))
    cursor.execute("SELECT COUNT(*) FROM Users WHERE group_num = (?)", (num,))
    count = cursor.fetchone()[0]

    if count > 0:
        split_amount = purchase_amount / count
        print(f"Total members in group {num}: {count}")
        print(f"Each member should pay: ${split_amount:.2f}")
    else:
        print(f"No members found in group {num}.")

def getUserID():
    user = input("Enter your username: ")
    cursor.execute("SELECT user_id FROM Users WHERE username = ?", (user,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print("Username not found.")
        return None

def userPurchases():
    user = getUserID()
    cursor.execute("""
            SELECT expense_id, category_id, amount, date, description 
            FROM Expenses 
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user,))
    purchases = cursor.fetchall()
    if purchases:
        print(f"\nPurchases made by User ID {user}:")
        for expense_id, category_id, amount, date, description in purchases:
            print(f"Expense ID: {expense_id}, Category: {category_id}, Amount: ${amount:.2f}, Date: {date}, Description: {description}")
    else:
        print("No purchases found for this user.")

userPurchases()

# To send changes to DB
connection.commit()

# To close DB
cursor.close()
connection.close()
print('SQLite Connection closed')

