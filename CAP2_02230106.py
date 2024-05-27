import os
import json
import random
import string

# Initialize the list to hold bank account objects
bank_accounts = []

# Define the BankAccount class with methods for deposit, withdrawal, and transfer operations
class BankAccount:
    def __init__(self, acc_num, acc_type, bal=0):
        self.acc_num = acc_num
        self.acc_type = acc_type
        self.bal = bal

    # Deposit method to increase the account balance
    def deposit(self, amt):
        self.bal += amt
        print(f"Deposited {amt}. New balance: {self.bal}")
        self.update_account_balance()

    # Withdrawal method to decrease the account balance
    def withdraw(self, amt):
        if self.bal >= amt:
            self.bal -= amt
            print(f"Withdrew {amt}. New balance: {self.bal}")
            self.update_account_balance()
        else:
            print("Insufficient balance.")

    # Transfer method to move funds between accounts
    def transfer(self, recipient_acc, amt):
        if self.bal >= amt:
            self.withdraw(amt)
            recipient_acc.deposit(amt)
            self.update_account_balance()
            recipient_acc.update_account_balance()
            print(f"Transferred {amt} to account {recipient_acc.acc_num}.")
        else:
            print("Insufficient balance.")

    # Method to update the account balance in the accounts list and file
    def update_account_balance(self):
        for account_dict in bank_accounts:
            if account_dict["acc_num"] == self.acc_num:
                account_dict["bal"] = self.bal
                break

        with open("bank_accounts.txt", "w") as file:
            json.dump(bank_accounts, file, default=lambda obj: obj.__dict__)

# Define the Account class, inheriting from BankAccount
class Account(BankAccount):
    def __init__(self, acc_num, acc_type, pwd, bal=0):
        super().__init__(acc_num, acc_type, bal)
        self.pwd = pwd

# Function to create a new account
def create_account():
    acc_type = input("Enter account type (Personal(p)/Business(b)): ").lower()
    if acc_type == "personal" or acc_type == "p":
        acc_type_str = "Personal"
    elif acc_type == "business" or acc_type == "b":
        acc_type_str = "Business"
    else:
        print("Invalid account type.")
        return

    acc_num = generate_acc_num()
    pwd = generate_pwd()
    acc = Account(acc_num, acc_type_str, pwd)
    print(f"{acc_type_str} account created. Account number: {acc_num}, Password: {pwd}")
    save_account(acc)

# Function to generate a unique account number
def generate_acc_num():
    return str(len(bank_accounts) + 1).zfill(3)

# Function to generate a secure password using ASCII letters and digits
def generate_pwd():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=5))

# Function to save an account object to the accounts list and file
def save_account(acc):
    bank_accounts.append(acc.__dict__)
    with open("bank_accounts.txt", "w") as file:
        json.dump(bank_accounts, file, default=lambda obj: obj.__dict__)

# Function to log in to an account by matching the entered account number and password
def login():
    acc_num = input("Enter your account number: ")
    for account_dict in bank_accounts:
        if account_dict["acc_num"] == acc_num:
            pwd = input("Enter your password: ")
            if account_dict["pwd"] == pwd:
                return Account(**account_dict)
            else:
                print("Invalid password.")
    print("Invalid account number.")

# Function to delete an account from the accounts list and file
def delete_account(acc):
    bank_accounts.remove(acc.__dict__)
    with open("bank_accounts.txt", "w") as file:
        json.dump(bank_accounts, file, default=lambda obj: obj.__dict__)
    print("Account deleted successfully.")

# Load existing accounts from the file if it exists
if os.path.exists("bank_accounts.txt"):
    with open("bank_accounts.txt", "r") as file:
        bank_accounts = json.load(file)

# Main program loop to interact with the user
while True:
    print("Welcome to My Bank. Are you a new customer? If yes then, please create an account or sign up or if you are an existing customer, please Sign in.")
    print("0. Create Account/Sign Up")
    print("1. Sign In")
    print("2. Logout/Exit")
    choice = input("Enter your option: ")

    if choice == "0":
        create_account()
    elif choice == "1":
        acc = login()
        if acc:
            print(f"Welcome to your {acc.acc_type} account!")
            while True:
                print("Check Balance - (press 1)")
                print("Deposit - (press 2)")
                print("Withdraw - (press 3)")
                print("Transfer - (press 4)")
                print("Delete Account - (press 5)")
                print("Sign out - (press 6)")
                option = input("Enter your option: ")

                if option == "1":
                    print(f"Your Balance is: {acc.bal}")
                elif option == "2":
                    amt = float(input("Enter your amount to deposit: "))
                    acc.deposit(amt)
                elif option == "3":
                    amt = float(input("Enter your amount to withdraw: "))
                    acc.withdraw(amt)
                elif option == "4":
                    recipient_num = input("Enter the recipient account number: ")
                    recipient = next((a for a in bank_accounts if a["acc_num"] == recipient_num), None)
                    if recipient:
                        recipient = Account(**recipient)
                        amt = float(input("Enter amount to transfer: "))
                        acc.transfer(recipient, amt)
                    else:
                        print("Invalid recipient account number.")
                elif option == "5":
                    delete_account(acc)
                    break
                elif option == "6":
                    break
                else:
                    print("Invalid option.")
    elif choice == "2":
        break
    else:
        print("Invalid choice.")
