import sqlite3
from datetime import datetime

# Connect to DB
connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()
print('Database Initialized')

def showAllUsers():
    cursor.execute("SELECT rowid, * FROM Users")
    people = cursor.fetchall()
    for person in people:
        print(f"{person}")

def showGroupusers(groupNum = None):
    if groupNum is None:
        groupNum = input("Enter group num: ")
    cursor.execute("SELECT * FROM Users WHERE group_num = ?", (groupNum,))
    people = cursor.fetchall()
    if people:
        print(f"\nMembers of Group {groupNum}:")
        for person in people:
            print(person)
    else:
        print(f"No members found in Group {groupNum}.")
   
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
    connection.commit()
    print(f"\nNew group created with Group Number {groupNum}. Here are the current group members:")
    showGroupusers(groupNum)
    
def joinGroup():
    groupNum = input("Enter the number of the group you wish to join: ")
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    userID = getHighestUserID() + 1
    cursor.execute("INSERT INTO Users VALUES (?,?,?,?)", (userID , user, password, groupNum))
    connection.commit()
    print(f"\nUser added to Group Number {groupNum}. Here are the current group members:")
    showGroupusers(groupNum)

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

def monthUserPurchases():
    user = getUserID()
    cursor.execute("""
            SELECT date 
            FROM Expenses 
            WHERE user_id = ?
            ORDER BY date DESC 
            LIMIT 1
            """, (user,))
    recent_date_row = cursor.fetchone()
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
        print(f"\nPurchases made by User ID {user} in {recent_date.strftime('%B %Y')}:")
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

# To send changes to DB
connection.commit()

# To close DB
cursor.close()
connection.close()
print('SQLite Connection closed')

