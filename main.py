import json
import os
import bcrypt


user_dict = {
    'prabin':'password1'
}

def load_user_data():
    filename = 'user.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {} 

def save_user_data(user_data):
    filename = 'user.json'
    with open(filename, 'w') as file:
        json.dump(user_data, file)

def load_deposit_list(username):
    filename = f"{username}_deposits.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    return[]
            except json.JSONDecodeError:
                return[]
    return[]              

def save_deposit_list(username, deposit_list):
    filename = f"{username}_deposits.json"
    with open(filename, 'w') as file:
        json.dump(deposit_list, file)


def append_deposit_to_list(username, amount_deposited):
    deposit_list = load_deposit_list(username)
    print(f"Before appending: {deposit_list}")
    deposit_list.append(amount_deposited)
    save_deposit_list(username, deposit_list)
    print(f"Deposit of ${amount_deposited} has been deposited to {username}'s deposit list")
    print(f"{username}'s deposit history {deposit_list}")

def sign_up():
    user_data  = load_user_data()
    while True:
        username = input("Create new username: ")
        if username in user_data:
            print("Username already exists try a different one")
        else:
            password = input("Create a new password:")
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_data[username] = hashed_password
            save_user_data(user_data)
            print(f"User {username}, successfully registered")
            break 

def login():
    user_data = load_user_data()
    
    username = input("Enter your username: ")
    if username in user_data:
        password = input("Enter your password: ")
        stored_hashed_password = user_data[username].encode('utf-8')

        # Checking if the provided password matches the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            print("Login Successful")
            return username
        else:
            print('Incorrect password, try again')
    else:        
        print("No account with that username, create a new acccount")



def deposit(username):
    while True:
        amount = input("Enter amount you want to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                append_deposit_to_list(username, amount)
                break
            else:
                print("Amount must be greater than 0")
        else:
            print("Please enter valid amount")

def withdrawal(username):
    current_balance = sum(load_deposit_list(username))
    print(f"Your current balance is {current_balance}")

    while True:
        withdraw_amount = input("Enter the amount you want to withdraw: ")
        if withdraw_amount.isdigit():
            withdraw_amount = int(withdraw_amount)

            if withdraw_amount > current_balance:
                print("Insufficient balance")
            else:
                print(f"You have successfully withdrawn ${withdraw_amount}")

                deposit_list = load_deposit_list(username)
                deposit_list.append(-withdraw_amount)

                save_deposit_list(username, deposit_list)
                break   

        else:
            print("Please enter a valid amount")



def main():

    while True:
        choice = input("Do you want to (1) Sign Up, (2) Log In, or (3) Exit the application? Enter 1, 2, or 3: ")
        if choice == '1':
            sign_up()
        elif choice == '2':
            username = login()
            if username:
                while True:
                    action = input(f"Welcome, {username}! Would you like to (w) Withdraw or (d) Deposit? Enter 'e' to exit: ").lower()
                    if action == 'w':
                        withdrawal(username)
                    elif action == 'd':
                        deposit(username)
                    elif action == 'e':
                        print("Goodbye")
                        break
                    else:
                        print("Invalid input, enter 'e','w', or 'd'")
        elif choice == '3':
            print("Exiting the application, Goodbye!")
            break                                
        else:
            print("Invalid choice. Please enter 1 or 2.")

main()


        