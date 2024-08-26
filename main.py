from urls import UrlPatterns
from bank import Bank
from colorama import Fore, Back, Style

def main():
    bank = Bank()
    url_patterns = UrlPatterns().urlpatterns
    while True:
        print(Fore.RED + 'Welcome to SIS Bankings!')
        print(Fore.GREEN + '1. Create User')
        print(Fore.BLUE + "2. Withdrawal")
        print(Fore.CYAN + "3. Deposit")
        print(Fore.YELLOW + "4. Check Statement")
        print(Fore.GREEN + "5. Transfer")
        print(Style.DIM + '6. Exit')
        print(Style.RESET_ALL)

        def func(choice):
            choice_str = str(choice) + "/" 
            for pattern, method in url_patterns:
                if choice_str == pattern:
                    if method():
                        return True
                    break
            else:
                print(Fore.RED + "Error 404. URL not found")
            return False

        try:
            choice = int(input("Enter your choice (1-6): "))
            if choice < 1 or choice > 6:
                raise ValueError
        except ValueError:
            print("Invalid choice. Please try again.")
            continue

        if choice == 1:
            print(Fore.GREEN + 'http://127.0.0.1/signup')
            bank.create_user()
        elif choice == 2:
            print(Fore.GREEN +'http://127.0.0.1/withdrawal')
            func(choice)    
        elif choice == 3:
            print(Fore.GREEN +'http://127.0.0.1/deposit')
            func(choice)
        elif choice == 4:
            print(Fore.GREEN +'http://127.0.0.1/check_statement')
            func(choice)
        elif choice == 5:
            print(Fore.GREEN +'http://127.0.0.1/transfer')
            if not func(choice):
                continue
        elif choice == 6:
            print(Fore.GREEN +'http://127.0.0.1/logout')
            print(Fore.RED +"Exiting...")
            print(Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()
