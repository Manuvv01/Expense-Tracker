import sqlite3
import os
from datetime import datetime

# Connect to DB
connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()

print('Database Initialized')

# Global variable to store logged-in user session
user_session = {}

if os.path.exists('Database for Expense tracker.db'):
    pass

def login_or_create_account():
    global user_session

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
                
                user_session['user_id'] = user[0]
                user_session['username'] = user[1]
                user_session['group_num'] = user[3]
                break
            else:
                print("Incorrect username or password. Please try again.")

        elif createOrLog == "0":
            print("Exiting program.")
            exit()  
        else:
            print("Invalid option. Please enter 1, 2, or 0.")

def is_user_logged_in():
    return 'user_id' in user_session

def showAllUsers():
    cursor.execute("SELECT rowid, * FROM Users")
    people = cursor.fetchall()
    for person in people:
        print(f"{person}")

def showGroupUsers():
    if not is_user_logged_in():
        print("Please log in to access this feature.")
        return

    group_num = user_session['group_num']
    cursor.execute("SELECT * FROM Users WHERE group_num = ?", (group_num,))
    people = cursor.fetchall()
    print(f"Users in your group ({group_num}):")
    for person in people:
        print(f"{person}")

def splitPurchase():
    if not is_user_logged_in():
        print("Please log in to access this feature.")
        return

    group_num = user_session['group_num']
    purchase_amount = float(input("Enter total purchase amount: "))
    cursor.execute("SELECT COUNT(*) FROM Users WHERE group_num = ?", (group_num,))
    count = cursor.fetchone()[0]

    if count > 0:
        split_amount = purchase_amount / count
        print(f"Total members in group {group_num}: {count}")
        print(f"Each member should pay: ${split_amount:.2f}")
    else:
        print(f"No members found in group {group_num}.")

def userPurchases():
    if not is_user_logged_in():
        print("Please log in to access this feature.")
        return

    user_id = user_session['user_id']
    cursor.execute("""
        SELECT expense_id, category_id, amount, date, description 
        FROM Expenses 
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    purchases = cursor.fetchall()

    if purchases:
        print(f"\nPurchases made by {user_session['username']}:")
        for expense_id, category_id, amount, date, description in purchases:
            print(f"Expense ID: {expense_id}, Category: {category_id}, Amount: ${amount:.2f}, Date: {date}, Description: {description}")
    else:
        print("No purchases found for this user.")

def monthUserPurchases():
    if not is_user_logged_in():
        print("Please log in to access this feature.")
        return

    user_id = user_session['user_id']
    cursor.execute("""
        SELECT date 
        FROM Expenses 
        WHERE user_id = ?
        ORDER BY date DESC 
        LIMIT 1
    """, (user_id,))
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
    """, (user_id, str(recent_year), f"{recent_month:02}"))
    expenses = cursor.fetchall()

    if expenses:
        print(f"\nPurchases made by {user_session['username']} in {recent_date.strftime('%B %Y')}:")
        for expense_id, category_id, amount, date, description in expenses:
            print(f"Expense ID: {expense_id}, Category: {category_id}, Amount: ${amount:.2f}, Date: {date}, Description: {description}")
    else:
        print("No purchases found for the most recent month.")

def main_menu():
    while True:
        print("\n--- Expense Tracker Menu ---")
        print(f"Logged in as: {user_session.get('username', 'Unknown')}")
        print("1. Show group members")
        print("2. Split group purchase")
        print("3. View user purchases")
        print("4. View user monthly purchases")
        print("5. Quit")

        choice = input("Please select an option (1-5): ")

        if choice == "1":
            showGroupUsers()
        elif choice == "2":
            splitPurchase()
        elif choice == "3":
            userPurchases()
        elif choice == "4":
            monthUserPurchases()
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

# Log in or create an account
login_or_create_account()

# Start the main menu
main_menu()

# Commit changes and close DB
connection.commit()
cursor.close()
connection.close()
print('SQLite Connection closed.')
