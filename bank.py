import csv
import pickle, random, string

class InsufficientBalanceError(Exception):
    pass

class IncorrectPINError(Exception):
    pass

class AccountDoesNotexists(Exception):
    pass

class User:
    def __init__(self, account_number, name, balance=0, pin=""):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        self.pin = pin

class Bank:
    def __init__(self):
        self._users = {}
        self._load_users_data()

    def _load_users_data(self):
        try:
            with open("users.bin", "rb") as file:
                self._users = pickle.load(file)
        except FileNotFoundError:
            print("No user data found. Starting with an empty database.")

    def _save_users_data(self):
        with open("users.bin", "wb") as file:
            pickle.dump(self._users, file)

    def add_user(self, user):
        self._users[user.account_number] = user
        self._save_users_data()

    #This method seems straightforward and should 
    #return the user object associated with the given 
    #account number from the _users dictionary.
    def get_user(self, account_number):
        user = self._users.get(account_number)
        print(f"Retrieved user: {user}")
        return user

    def create_user(self):
        account_number = ''.join(random.choices(string.digits, k=10))
        name = input("Enter name: ")
        initial_balance = float(input("Enter initial balance: "))
        pin = input("Enter account PIN: ")
        user = User(account_number, name, initial_balance, pin)
        self.add_user(user)
        print("User created successfully.")
        print(f"Account Number: {account_number}")

        self.write_statement(account_number, initial_balance)

    def authenticate_user(self, account_number, pin):
        user = self.get_user(account_number)
        print(f"User found: {user}")
        if user and user.pin == pin:
            return True
        return False
    
    def write_transfer_details(self, sender_account_number, receiver_account_number, amount):
        with open("transfer_details.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([sender_account_number, receiver_account_number, amount])

    def write_statement(self,account_number, statement):
        with open("account_statement.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([account_number, statement])

    def account_exists(self, account_number):
        with open("account_statement.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == account_number:
                    return True
        return False

    @staticmethod
    def deposit_money(user, amount):
        user.balance += amount

    @staticmethod
    def withdraw_money(user, amount):
        if user.balance < amount:
            raise InsufficientBalanceError("Insufficient balance for withdrawal")
        user.balance -= amount

    def check_account_details(self, account_number, pin):
        if not self.authenticate_user(account_number, pin):
            raise IncorrectPINError("Incorrect PIN or account number")
        user = self.get_user(account_number)
        print(f"Account Number: {user.account_number}")
        print(f"Name: {user.name}")
        print(f"Balance: {user.balance}")

    def deposit(self, account_number, pin, amount):
        print('Deposit started')
        if not self.authenticate_user(account_number, pin):
            raise IncorrectPINError("Authentication failed! Incorrect PIN or account number")
        print("User authenticated successfully.")
        user = self.get_user(account_number)
        if user:
            print("User found.")
        else:
            print("User not found.")
        user.balance += amount
        print(f"New balance after deposit: {user.balance}")
        print("Deposit successful.")
        self.write_statement(account_number, user.balance) 

    def withdraw(self, account_number, pin, amount):
        if not self.authenticate_user(account_number, pin):
            raise IncorrectPINError("Incorrect PIN or account number")
        print("User authenticated successfully.")
        user = self.get_user(account_number)
        if user:
            print("User found.")
        else:
            print("User not found.")
        if user.balance < amount:
            raise InsufficientBalanceError("Insufficient balance for withdrawal")
        user.balance -= amount
        print(f"New balance after withdrawal: {user.balance}")
        print("Withdrawal successful.")
        self.write_statement(account_number, user.balance)

    def transfer(self, sender_account_number, sender_pin, receiver_account_number, amount):
        sender = self.get_user(sender_account_number)
        if not sender or sender.pin != sender_pin:
            raise IncorrectPINError("Incorrect PIN or account number")
        receiver = self.get_user(receiver_account_number)
        if not receiver:
            print("Receiver account not found.")
            return False
        if sender.balance < amount:
            raise InsufficientBalanceError("Insufficient balance for transfer")
        self.withdraw_money(sender, amount)
        self.deposit_money(receiver, amount)
        print("Transfer successful.")
        self.write_transfer_details(sender_account_number, receiver_account_number, amount)
        return True