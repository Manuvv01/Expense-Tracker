import sqlite3
import os
from datetime import datetime

# Connect to DB
connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()

print('Database Initialized')

if os.path.exists('Database for Expense tracker.db'):
    pass

while True:
    createOrLog = input("Enter 1 to create an account, 2 to log in, or 0 to exit: ")

    if createOrLog == "1":
        username = input("Enter account username: ")
        password = input("Enter account password: ")
        try:
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", [username, password])
            connection.commit()
            print("Account successfully created!")
        except sqlite3.IntegrityError:
            print("Username already exists. Please try a different one.")

    elif createOrLog == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")

        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", [username, password])
        user = cursor.fetchone()

        if user:
            print("Logged in successfully!")
            break
        else:
            print("Incorrect username or password. Please try again.")

    elif createOrLog == "0":
        print("Exiting program.")
        break
    else:
        print("Invalid option. Please enter 1, 2, or 0.")

def showAllUsers():
    cursor.execute("SELECT rowid, * FROM Users")
    people = cursor.fetchall()
    for person in people:
        print(f"{person}")

def showGroupUsers():
    num = input("Enter group number: ")
    cursor.execute("SELECT * FROM Users WHERE group_num = ?", (num,))
    people = cursor.fetchall()
    for person in people:
        print(f"{person}")

def getHighestGroup():
    cursor.execute("SELECT MAX(group_num) FROM Users")
    highGroupNum = cursor.fetchone()[0]
    return highGroupNum if highGroupNum else 0

def getHighestUserID():
    cursor.execute("SELECT MAX(user_id) FROM Users")
    highUserID = cursor.fetchone()[0]
    return highUserID if highUserID else 0

def createNewGroup():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    groupNum = getHighestGroup() + 1
    userID = getHighestUserID() + 1
    try:
        cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (userID, username, password, groupNum))
        connection.commit()
        print(f"New group {groupNum} created successfully!")
    except sqlite3.IntegrityError:
        print("Error creating a new group. Please try again.")

def joinGroup():
    groupNum = input("Enter the number of the group you wish to join: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Validate that the group exists
    cursor.execute("SELECT 1 FROM Users WHERE group_num = ?", (groupNum,))
    if not cursor.fetchone():
        print(f"Group {groupNum} does not exist.")
        return

    userID = getHighestUserID() + 1
    try:
        cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (userID, username, password, groupNum))
        connection.commit()
        print(f"User {username} joined group {groupNum} successfully!")
    except sqlite3.IntegrityError:
        print("Error joining the group. Please try again.")

def splitPurchase():
    groupNum = input("Enter group number: ")
    purchase_amount = float(input("Enter total purchase amount: "))
    cursor.execute("SELECT COUNT(*) FROM Users WHERE group_num = ?", (groupNum,))
    count = cursor.fetchone()[0]

    if count > 0:
        split_amount = purchase_amount / count
        print(f"Total members in group {groupNum}: {count}")
        print(f"Each member should pay: ${split_amount:.2f}")
    else:
        print(f"No members found in group {groupNum}.")

def getUserID(username):
    cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print("Username not found.")
        return None

def userPurchases():
    username = input("Enter your username: ")
    user = getUserID(username)

    if user:
        cursor.execute("""
            SELECT expense_id, category_id, amount, date, description 
            FROM Expenses 
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user,))
        purchases = cursor.fetchall()

        if purchases:
            print(f"\nPurchases made by {username}:")
            for expense_id, category_id, amount, date, description in purchases:
                print(f"Expense ID: {expense_id}, Category: {category_id}, Amount: ${amount:.2f}, Date: {date}, Description: {description}")
        else:
            print("No purchases found for this user.")

def monthUserPurchases():
    username = input("Enter your username: ")
    user = getUserID(username)

    if user:
        cursor.execute("""
            SELECT date 
            FROM Expenses 
            WHERE user_id = ?
            ORDER BY date DESC 
            LIMIT 1
        """, (user,))
        recent_date_row = cursor.fetchone()

        if not recent_date_row:
            print("No expenses found for this user.")
            return

        recent_date = datetime.strptime(recent_date_row[0], '%Y-%m-%d')
        recent_year = recent_date.year
        recent_month = recent_date.month

        cursor.execute("""
            SELECT expense_id, category_id, amount, date, description 
            FROM Expenses 
            WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
            ORDER BY date DESC
        """, (user, str(recent_year), f"{recent_month:02}"))
        expenses = cursor.fetchall()

        if expenses:
            print(f"\nPurchases made by {username} in {recent_date.strftime('%B %Y')}:")
            for expense_id, category_id, amount, date, description in expenses:
                print(f"Expense ID: {expense_id}, Category: {category_id}, Amount: ${amount:.2f}, Date: {date}, Description: {description}")
        else:
            print("No purchases found for the most recent month.")

def main_menu():
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Create new group")
        print("2. Join existing group")
        print("3. Split group purchase")
        print("4. User breakdown of expenses")
        print("5. User monthly breakdown of expenses")
        print("6. Quit")
        
        choice = input("Please select an option (1-6): ")

        if choice == "1":
            createNewGroup()
        elif choice == "2":
            joinGroup()
        elif choice == "3":
            splitPurchase()
        elif choice == "4":
            userPurchases()
        elif choice == "5":
            monthUserPurchases()
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

# Start the program
main_menu()

# Commit changes and close DB
connection.commit()
cursor.close()
connection.close()
print('SQLite Connection closed.')
