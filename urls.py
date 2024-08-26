from bank import Bank, IncorrectPINError, InsufficientBalanceError

class get_details:
    bank = Bank()
    def withdraw(self):
        account_number = input("Enter user account number: ")
        pin = input("Enter account PIN: ")
        try:
            amount = float(input("Enter amount to withdraw: "))
            self.bank.withdraw(account_number, pin, amount)
            print('withdrawal calls')
        except (InsufficientBalanceError, IncorrectPINError, ValueError) as e:
            print(f"Error: {e}")

    def deposit(self):
        account_number = input("Enter user account number: ")
        pin = input("Enter account PIN: ")
        try:
            if not account_number:
                raise ValueError("Account number cannot be empty")
            amount = float(input("Enter amount to deposit: "))
            self.bank.deposit(account_number, pin, amount)
        except (IncorrectPINError, ValueError) as e:
            print(f"Error: {e}")

    
    def check_account_details(self):
        account_number = input("Enter user account number: ")
        if not account_number:
            print("Account number cannot be empty")
            return
        pin = input("Enter account PIN: ")
        if not pin:
            print("PIN cannot be empty")
            return
        if self.bank.account_exists(account_number):
            try:
                self.bank.check_account_details(account_number, pin)
            except IncorrectPINError as e:
                print(f"Error: {e}")
        else:
            print('Account does not exist! Please check account number. ')
            
    def transfer(self):
        while True:
            sender_account_number = input("Enter sender's account number: ")
            sender_pin = input("Enter sender's account PIN: ")
            receiver_account_number = input("Enter receiver's account number: ")
            try:
                amount = float(input("Enter amount to transfer: "))
            except ValueError as e:
                print('Error', e)
                continue
            try:
                self.bank.transfer(sender_account_number, sender_pin, receiver_account_number, amount)
            except (InsufficientBalanceError, IncorrectPINError) as e:
                print(f"Error: {e}")
            break

class UrlPatterns(get_details):
    def __init__(self):
        self.this = get_details()
        self.urlpatterns = [
            ("1/", "create_user"),
            ("2/", self.this.withdraw),
            ("3/", self.this.deposit),
            ("4/", self.this.check_account_details),
            ("5/", self.this.transfer),
        ]