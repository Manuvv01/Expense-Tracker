import sqlite3
import os
from datetime import datetime

# Connect to DB
connection = sqlite3.connect('Database for Expense tracker.db')
cursor = connection.cursor()

print('Database Initialized')
user_session = {}

os.system('cls')


def login_or_create_account():
    global user_session

    while True:
        createOrLog = input("Enter 1 to create an account, 2 to log in, or 0 to exit: ")
        
        os.system('cls')

        if createOrLog == "1":
            username = input("Enter account username: ")
            password = input("Enter account password: ")

            os.system('cls')

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
            os.system('cls')
            if user:
                print("Logged in successfully!")
                os.system('cls')
                user_session['user_id'] = user[0]
                user_session['username'] = user[1]
                user_session['group_num'] = user[3]
                break
            else:
                print("Incorrect username or password. Please try again.")

        elif createOrLog == "0":
            print("Exiting program.")
            exit()  

            os.system('cls')

        else:
            print("Invalid option. Please enter 1, 2, or 0.")

def is_user_logged_in():
    return 'user_id' in user_session
def enterExpense():
    os.system('cls')
    user_id = user_session['user_id']
    while True:

        amountInput = input("Enter amount of purchase: ")
        try:
            amount = float(amountInput)
            if amount < 0:
                print("The amount entered should be positive, please try again.")
            else:
                break
        except ValueError:
            print("Please enter a number, do not use letters.")
            return
    while True:
        Newdate = input("Enter the date of purchase (YYYY-MM-DD): ")
        try:
            datetime.strptime(Newdate, '%Y-%m-%d')
            break
            
        except ValueError:
            print("Invalid date format. Please enter the date as YYYY-MM-DD.")
            

    description = input("Enter description of purchase(gas, food,etc...): ")

    while True:
        category_options = {
            "1": "food",
            "2": "gas",
            "3": "transportation",
            "4": "shopping",
            "5": "subscriptions"
            }

        category_id = input("Enter a category for this expense:\n1. food\n2. gas\n3. transportation\n4. shopping\n5. subscriptions\n")

        if category_id in category_options:
            category = int(category_id)
            break

        else:
            print("Invalid category. Please enter a category that would fit the description")

    try:
        cursor.execute("INSERT INTO Expenses (user_id, amount, date, description, category_id) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, Newdate, description, category,)
        )
        connection.commit()
        print("New expense has been added successfully!")

    except sqlite3.Error as e:
        print(f"An unexpected error has occured while trying to add your new expense. Please try again: {e}")
            

def showGroupUsers():
    os.system('cls')
    group_num = user_session['group_num']
    cursor.execute("SELECT * FROM Users WHERE group_num = ?", (group_num,))
    people = cursor.fetchall()
    print(f"Users in your group ({group_num}):")
    for person in people:
        print(f"{person}")
def splitPurchase():
    os.system('cls')
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
    os.system('cls')
    user_id = user_session['user_id']
    cursor.execute("SELECT amount, date, description FROM Expenses WHERE user_id=?", (user_id,))
    purchases = cursor.fetchall()
    
    if purchases:
        print(f"\nPurchases made by {user_session['username']}:")
        for amount, date, description in purchases:
            print(f"Amount: ${amount:.2f}, \nDate: {date}, \nDescription: {description} \n-------------------")
       
    else:
        print("No purchases found for this user.")

def monthUserPurchases():
    os.system('cls')
    user_id = user_session['user_id']

    cursor.execute("SELECT date FROM Expenses WHERE user_id=? ORDER BY date DESC", (user_id,))
    recent_date_row = cursor.fetchone()

    if not recent_date_row:
        print("No expenses found for this user.")
    
    recent_date = datetime.strptime(recent_date_row[0], '%Y-%m-%d')
    recent_year = recent_date.year
    recent_month = recent_date.month
    
    cursor.execute("""
        SELECT amount, date, description 
        FROM Expenses 
        WHERE user_id = ? 
        AND strftime('%Y', date) = ?
        AND strftime('%m', date) = ?
        ORDER BY date DESC
    """, (user_id, str(recent_year), f"{recent_month:02}"))
    expenses = cursor.fetchall()
    
    if expenses:
        print(f"\nPurchases made by {user_session['username']} for the most recent dates:\n----------------------------------------------------")
        for amount, date, description in expenses:
            print(f"In {recent_date.strftime('%B %Y')}:")
            print(f"Amount: ${amount:.2f}, Date: {date}, Description: {description} \n----------------------------------------------------")
            
    else:
        print("No purchases found for the most recent months.")
    
def main_menu():
    while True:
        print("\n--- Expense Tracker Menu ---")
        print(f"Logged in as: {user_session.get('username', 'Unknown')}")
        print("1. Enter New Expense")
        print("2. Show group members")
        print("3. Split group purchase")
        print("4. View user purchases")
        print("5. View user monthly purchases")
        print("6. Quit")

        choice = input("Please select an option (1-6): ")

        if choice == "1":
            os.system('cls')
            enterExpense()

        elif choice == "2":
            os.system('cls')
            showGroupUsers()

        elif choice == "3":
            os.system('cls')
            splitPurchase()

        elif choice == "4":
            os.system('cls')
            userPurchases()

        elif choice == "5":
            os.system('cls')
            monthUserPurchases()
            
        elif choice == "6":
            os.system('cls')
            print("Exiting the program.")
            break 
            
        else:
            os.system('cls')
            print("Invalid choice. Please enter a number from 1 to 5.")
            
login_or_create_account()

main_menu()

connection.commit()
cursor.close()
connection.close()
print('SQLite Connection closed.')
