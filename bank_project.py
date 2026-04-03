import random
import datetime
import json
import hashlib
import os

class InvalidAmount(Exception):
    pass

class InsufficientFund(Exception):
    pass


class Account:
    __password = ""
    _account_number = 0
    _fname = ""
    _lname = ""
    _is_valid_user = False

    def __init__(self):
        pass

    def __create_new_pass(self):
        while True:
            __passwd_input = input("Enter the password (or 'q' to cancel) : ").strip()
            if __passwd_input.lower() == "q":
                print("Password creation cancelled.")
                return False
            __passwd_input_check = input("Re-enter your password : ").strip()
            if __passwd_input_check.lower() == "q":
                print("Password creation cancelled.")
                return False
            if (__passwd_input == __passwd_input_check) and (__passwd_input != ""):
                password_hash = hashlib.sha512()
                password_hash.update(__passwd_input.encode('utf-8'))
                self.__password = password_hash.hexdigest()
                print("Your password set sucessfully !")
                return True
            else:
                print("Both password and re-entering should be the same, please try again.")

    def __create_new_accno(self):
        __assign_accno = random.randint(10**(14), (10**15) - 1)
        self._account_number = __assign_accno

    def __user_detail(self):
        input_fname = input("What is your first name ? : ").strip()
        input_lname = input("What is your last name ? : ").strip()
        choice_name = input(f"\nYour name is {input_fname} {input_lname}, is that correct? [y/n] : ").strip().lower()

        if (choice_name == "y" or choice_name == "yes") and (input_fname != "" and input_lname != ""):
            self._fname = input_fname
            self._lname = input_lname
            print("\nYour name set sucsessfully !\n")

        elif choice_name == "n" or choice_name == "no":
            print("\nPlease re-enter your correct name.\n")
            self.__user_detail()
        
        else:
            print("\nYou enterd the wrong choice please try again.\n")
            self.__user_detail()

    def __update_new_accounts(self):
        try:
            with open("account_credentials.json","r") as jr:
                __fetched_credentials = json.load(jr)
            with open("account_credentials.json","w") as jw:
                __fetched_credentials.update({ self._account_number : self.__password})
                json.dump(__fetched_credentials, jw, indent=4)
        
        except (FileNotFoundError, json.JSONDecodeError):
            __acc_cred = {}
            with open("account_credentials.json","w") as jw:
                __acc_cred.update({ self._account_number : self.__password})
                json.dump(__acc_cred, jw, indent=4)

        try:
            with open("account_details.json","r") as jr:
                __fetched_data = json.load(jr)
            with open("account_details.json","w") as jw:
                __fetched_data[str(self._account_number)] = { "fname" : self._fname, "lname" : self._lname}
                json.dump(__fetched_data, jw, indent=4)
        
        except (FileNotFoundError, json.JSONDecodeError):
            __acc_dict = {}
            with open("account_details.json","w") as jw:
                __acc_dict[str(self._account_number)] = { "fname" : self._fname, "lname" : self._lname}
                json.dump(__acc_dict, jw, indent=4)

    def __clear_credentials(self):
        self.__password, self._fname, self._lname, self._account_number = "", "", "", 0
        

    def create_account(self):
        choice = input("You are creating new account in the bank, do you wish to proceed ? [y/n]").strip().lower()
        if choice == "y" or choice == "yes":
            self.__user_detail()
            self.__create_new_accno()
            if not self.__create_new_pass():
                self.__clear_credentials()
                self.final_msg()
                return None
            self.__update_new_accounts()
            print(f"""
            \nYou created new account with us.
            Please note your account number and save it carefully for the future uses :
            ACCOUNT NUMBER - {self._account_number}
            Now you can login with your credentials to use the banking services.""")
            self.__clear_credentials()
            self.final_msg()

        elif choice == "n" or choice == "no":
            self.final_msg()
        
        else:
            print("You enterd the wrong choice please try again.")
            self.create_account()

    def login_error(self):
        print("\nERROR - INVALID CREDENTIALS, EITHER ACCOUNT NUMBER OR PASSWORD IS INVALID, PLEASE TRY AGAIN.\n")

    def __validity_check(self):
        __input_accno = input("\nEnter the account number : ").strip()
        __input_pass = input("Enter your password : ")
        __input_pass_hash = hashlib.sha512()
        __input_pass_hash.update(__input_pass.encode('utf-8'))
        __input_pass_hash = __input_pass_hash.hexdigest()

        try:
            with open("account_credentials.json","r") as jr:
                 __fetched_credentials = json.load(jr)
        except (FileNotFoundError, json.JSONDecodeError):
            self.login_error()
            return

        if __fetched_credentials.get(__input_accno) == __input_pass_hash:
            self._account_number = int(__input_accno)
            self._is_valid_user = True
        else:
            self.login_error()

    def fetch_details(self):
        if self._is_valid_user:
            with open("account_details.json","r") as jr:
                __fetched_data = json.load(jr)

            accno_key = str(self._account_number)
            if accno_key in __fetched_data:
                account_info = __fetched_data[accno_key]
                self._fname = account_info["fname"]
                self._lname = account_info["lname"]
                return (self._fname, self._lname, self._account_number)
        else:
            pass

    def final_msg(self):
        print("\nThank you for using our banking services :D\n")

    def login(self):
        self.__validity_check()

    def logout(self):
        self.__clear_credentials()
        self.final_msg()

    def change_password(self):
        if not self._is_valid_user:
            self.login_error()
            return None

        try:
            with open("account_credentials.json","r") as jr:
                __fetched_credentials = json.load(jr)
        except (FileNotFoundError, json.JSONDecodeError):
            print("\nSomething went wrong, please try again later.\n")
            return None

        accno_key = str(self._account_number)
        if accno_key not in __fetched_credentials:
            self.login_error()
            return None

        current_pass = input("\nEnter your current password : ")
        current_pass_hash = hashlib.sha512()
        current_pass_hash.update(current_pass.encode('utf-8'))
        current_pass_hash = current_pass_hash.hexdigest()
        if __fetched_credentials.get(accno_key) != current_pass_hash:
            print("\nCurrent password is incorrect.\n")
            return None

        while True:
            new_pass = input("Enter new password (or 'q' to cancel): ").strip()
            if new_pass.lower() == "q":
                print("\nPassword change cancelled.\n")
                return None
            new_pass_check = input("Re-enter new password : ").strip()
            if new_pass_check.lower() == "q":
                print("\nPassword change cancelled.\n")
                return None
            if new_pass != new_pass_check:
                print("\nPasswords do not match, please try again.\n")
                continue
            if new_pass == "":
                print("\nPassword cannot be empty.\n")
                continue
            if new_pass == current_pass:
                print("\nNew password cannot be same as current password.\n")
                continue
            break

        new_pass_hash = hashlib.sha512()
        new_pass_hash.update(new_pass.encode('utf-8'))
        __fetched_credentials[accno_key] = new_pass_hash.hexdigest()
        with open("account_credentials.json","w") as jw:
            json.dump(__fetched_credentials, jw, indent=4)
        print("\nYour password has been changed successfully.\n")


class Transactions(Account):
    _balance_user = 0.0
    _capital_bank = 0.0
    _is_valid_user = False
    _account_number = 0
    _file_name = "transactions.json"


    def __init__(self):
        super().__init__()
        self._file_name = "transactions.json"

    def login(self):
        super().login()
        self._file_name = "transactions.json"

    def login_error(self):
        return super().login_error()
    
    def fetch_amount(self):
        try:
            with open(self._file_name,"r") as jr:
                __fetched_transactions = json.load(jr)
            accno_key = str(self._account_number)
            if accno_key in __fetched_transactions:
                self._balance_user = __fetched_transactions[accno_key].get("crrbal", 0.0)
            else:
                self._balance_user = 0.0
        except (FileNotFoundError, json.JSONDecodeError):
            self._balance_user = 0.0

    def update_amount(self, transection):
        try:
            with open(self._file_name,"r") as jr:
                __fetched_transactions = json.load(jr)
            with open(self._file_name,"w") as jw:
                accno_key = str(self._account_number)
                if accno_key not in __fetched_transactions:
                    __fetched_transactions[accno_key] = self.format_file(transection)
                else:
                    __fetched_transactions[accno_key]["crrbal"] = self._balance_user
                    __fetched_transactions[accno_key]["transactions"].insert(0, transection)
                json.dump(__fetched_transactions, jw, indent=4)
        
        except (FileNotFoundError, json.JSONDecodeError):
            __all_transactions = {}
            accno_key = str(self._account_number)
            __all_transactions[accno_key] = self.format_file(transection)
            with open(self._file_name,"w") as jw:
                json.dump(__all_transactions, jw, indent=4)

    @classmethod
    def fetch_bank_capital(cls):
        try:
            with open("bank_details.json","r") as jr:
                __bank_details = json.load(jr)
            cls._capital_bank = __bank_details.get("crrcapital", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Something went wrong please try again later.")
    
    @classmethod
    def update_bank_capital(cls):
        try:
            with open("bank_details.json","r") as jr:
                __bank_details = json.load(jr)
            __bank_details["crrcapital"] = cls._capital_bank
            with open("bank_details.json","w") as jw:
                json.dump(__bank_details, jw, indent=4)

        except (FileNotFoundError, json.JSONDecodeError):
            print("\nSomething went wrong, please try again later.\n")


    def format_transaction(self, amount, transaction_type):
        transaction = {
            "date": datetime.datetime.now().strftime("%d/%m/%Y %I:%M:%S %p"),
            "type": transaction_type,
            "amount": amount,
            "balance_after_transaction": self._balance_user
        }
        return transaction
    
    def format_file(self, transaction):
        formatted_data = {
            "crrbal": self._balance_user,
            "transactions": []
        }
        formatted_data["transactions"].insert(0, transaction)
        return formatted_data
    
        
    def deposite(self):
        if self._is_valid_user:
            try:
                self.fetch_amount()
                Transactions.fetch_bank_capital()
                amount = float(input("\nEnter the amount you want to deposite to the bank : "))
                if amount > 0:
                    self._balance_user += amount
                    Transactions._capital_bank += amount  # keep bank total on class variable
                    transaction = self.format_transaction(amount, "Deposite")
                    self.update_amount(transaction)
                    Transactions.update_bank_capital()
                    print(f"\nYou deposite {amount} successfully, your current balance is {self._balance_user}.\n")
                else:
                    raise InvalidAmount
            except (ValueError, InvalidAmount):
                print("\nThe entered amount is not valid, please enter valid amount that you want to deposite.")
        else:
            self.login_error()

    def withdraw(self):
        if self._is_valid_user:
            try:
                self.fetch_amount()
                Transactions.fetch_bank_capital()
                amount = float(input("\nEnter the amount you want to withdraw from the bank : "))
                if amount <= 0:
                    raise InvalidAmount
                if amount > self._balance_user:
                    raise InsufficientFund
                self._balance_user -= amount
                Transactions._capital_bank -= amount  # keep bank total on class variable
                transaction = self.format_transaction(amount, "Withdraw")
                self.update_amount(transaction)
                Transactions.update_bank_capital()
                print(f"\nYou withdrew {amount} successfully, your current balance is {self._balance_user}.\n")
            except ValueError:
                print("\nThe entered amount is not valid, please enter valid amount that you want to withdraw.")
            except InvalidAmount:
                print("\nThe amount must be greater than zero.")
            except InsufficientFund:
                print(f"\nInsufficient funds! Your current balance is {self._balance_user}. Please enter a smaller amount.")
        else:
            self.login_error()


class Loan(Transactions):
    _balance_user = 0.0
    _capital_bank = 0.0
    _account_number = 0
    _is_valid_user = False
    _loans = []
    _file_name = "transactions.json"
    _loan_types = ("Personal","Home","Car/Vehical","Educational")

    def __init__(self):
        super().__init__()

    @classmethod
    def fetch_bank_capital(cls):
        return super().fetch_bank_capital()
    
    @classmethod
    def update_bank_capital(cls):
        return super().update_bank_capital()
    
    def fetch_amount(self):
        return super().fetch_amount()
    
    def update_amount(self, transection):
        return super().update_amount(transection)
    
    def format_transaction(self, amount, transaction_type):
        return super().format_transaction(amount, transaction_type)
    
    def format_file(self, transaction):
        return super().format_file(transaction)
    
    def login_error(self):
        return super().login_error()
    
    def is_loan_available(self, loan_amount):
        Loan.fetch_bank_capital()
        if Loan._capital_bank >= loan_amount:
            return True
        else:
            return False
        
    def fetch_loans(self):
        try:
            with open("loan_details.json","r") as jr:
                loan_details = json.load(jr)
            accno_key = str(self._account_number)
            if accno_key in loan_details:
                self._loans = loan_details[accno_key]
            else:
                self._loans = []
        except (FileNotFoundError, json.JSONDecodeError):
            self._loans = []
    
    def update_new_loan(self, loan_details):
        with open("loan_details.json","w") as jw:
            json.dump(loan_details, jw, indent=4)

    def set_formattor_loan(self, loan_type, amount, emiamount, duration):
        try:
            with open("loan_details.json","r") as jr:
                loan_details = json.load(jr)
        except (FileNotFoundError, json.JSONDecodeError):
            loan_details = {}
        
        accno_key = str(self._account_number)
        if accno_key not in loan_details:
            loan_details[accno_key] = []
        
        loan_details[accno_key].append(self.format_new_loan(loan_type, amount, emiamount, duration))
        return loan_details
                    
    def format_emi(self, emiamount):
        month = int(datetime.datetime.now().strftime("%m"))
        year = int(datetime.datetime.now().strftime("%Y"))
        return f"({month}, {year})", emiamount


    def format_new_loan(self, loan_type, amount, emiamount, duration):
        loandetails = {
            "type":loan_type,
            "amount":amount,
            "intrestrate":7,
            "emiamount":emiamount,
            "duration":duration,
            "emidetails":{}
        }
        return loandetails

    
    def cal_emi(self,amount,duration):
        intrest_rate_month = 7/(12*100)
        intermediate_cal = (1+intrest_rate_month)**duration
        emi_amount = amount*intrest_rate_month*( intermediate_cal / (intermediate_cal-1))
        return emi_amount
    
    def take_loan(self):
        if self._is_valid_user:
            while True:
                try:
                    print("")
                    for counter, loan_type in enumerate(self._loan_types, start=1):
                        print(f"{counter} - {loan_type}")
                    choice_raw = input("\nPlease enter which type of loan you want to take (or 'q' to cancel) : ").strip().lower()
                    if choice_raw == "q":
                        print("\nLoan request cancelled.\n")
                        return None
                    choice_loan_type = int(choice_raw)
                    if choice_loan_type < 1 or choice_loan_type > len(self._loan_types):
                        raise ValueError
                    loan_type = self._loan_types[choice_loan_type-1]
                    break
                except (ValueError, IndexError):
                    print("\nPlease enter valid value as mentioned.\n")

            while True:
                try:
                    print("")
                    amount_raw = input("Enter amount of loan you want to take (or 'q' to cancel) : ").strip().lower()
                    if amount_raw == "q":
                        print("\nLoan request cancelled.\n")
                        return None
                    amount = float(amount_raw)
                    if amount <= 0.0:
                        raise ValueError
                    break
                except ValueError:
                    print("\nEnter the valid amount.\n")

            while True:
                try:
                    print("")
                    print("\nNote : You can take loan for maximum of 7 years, enter the duration in number of months\n")
                    tenure_raw = input("Enter the duration for your loan (or 'q' to cancel) : ").strip().lower()
                    if tenure_raw == "q":
                        print("\nLoan request cancelled.\n")
                        return None
                    tenure = int(tenure_raw)
                    if tenure <= 0 or tenure > 84:
                        raise ValueError
                    break
                except ValueError:
                    print("\nPlease read the note carefully and enter your duration.")
            
            emiamount = round(self.cal_emi(amount, tenure),2)

            loan_availablity = self.is_loan_available(amount)
            if loan_availablity:
                pass
            else:
                print("\nAt the moment we can't provide you the loan, please try again later.\n")
                return None
            

            print(f"""
            This is your details of the loan please read carefully.
            
            Type : {loan_type}
            Amount : {amount}
            Interest Rate : 7% per annum
            Duration : {tenure} Months
            EMI Amount : {emiamount}
            Interest Amount : {round(emiamount*tenure - amount,2)}
            Total Amount to be paid : {round(emiamount*tenure,2)}
            """)

            while True:
                choice_loan_process = input("\nDo you wish to proceed? [y/n or 'q' to cancel]").strip().lower()

                if choice_loan_process == "q":
                    print("\nLoan request cancelled.\n")
                    return None
                if choice_loan_process == "y" or choice_loan_process == "yes":
                    loan_details = self.set_formattor_loan(loan_type, amount, emiamount, tenure)
                    self.update_new_loan(loan_details)
                    Loan._capital_bank -= amount
                    Loan.update_bank_capital()
                    self.fetch_amount()
                    self._balance_user += amount
                    transaction = self.format_transaction(amount, f"{loan_type} Loan")
                    self.update_amount(transaction)
                    print("\nYour loan processed sucessfully !")
                    break
                    
                elif choice_loan_process == "n" or choice_loan_process == "no":

                    while True:
                        rechoice_input = input("\nDo you want to insert loan details again? [y/n or 'q' to cancel]").strip().lower()
                        if rechoice_input == "q":
                            return None
                        if rechoice_input == "y" or rechoice_input == "yes":
                            self.take_loan()
                        elif rechoice_input == "n" or rechoice_input == "no":
                            return None
                        else:
                            print("Please enter a valid input")

                else:
                    print("\nPlease enter a valid input")
        else:
            self.login_error()

    def pay_emi(self):
        if self._is_valid_user == False:
            self.login_error()
            return None

        self.fetch_loans()
        if not self._loans:
            print("\nYou have no active loans to pay EMI for.\n")
            return None

        print("")
        for counter, loan in enumerate(self._loans, start=1):
            print(
                f"{counter} - {loan.get('type', 'Loan')} | Amount: {loan.get('amount')} | "
                f"EMI: {loan.get('emiamount')} | Duration: {loan.get('duration')}"
            )

        while True:
            try:
                choice_raw = input("\nSelect the loan number to pay EMI (or 'q' to cancel): ").strip().lower()
                if choice_raw == "q":
                    print("\nEMI payment cancelled.\n")
                    return None
                choice_loan = int(choice_raw)
                if choice_loan < 1 or choice_loan > len(self._loans):
                    raise ValueError
                break
            except ValueError:
                print("\nPlease enter a valid loan number.\n")

        loan_index = choice_loan - 1
        selected_loan = self._loans[loan_index]
        selected_loan.setdefault("emidetails", {})
        emi_amount = selected_loan.get("emiamount")
        if emi_amount is None:
            print("\nEMI amount not found for this loan.\n")
            return None

        current_month = int(datetime.datetime.now().strftime("%m"))
        current_year = int(datetime.datetime.now().strftime("%Y"))
        emi_key = f"({current_month}, {current_year})"
        
        if emi_key in selected_loan["emidetails"]:
            print("\nThis month's EMI is already paid for this loan.\n")
            return None

        pay_choice = input("\nThis month's EMI is pending. Do you want to pay now? [y/n] ").strip().lower()
        if pay_choice not in ("y", "yes"):
            print("\nEMI payment cancelled.\n")
            return None

        try:
            self.fetch_amount()
            if self._balance_user < emi_amount:
                raise InsufficientFund

            emi_key, emi_amt = self.format_emi(emi_amount)
            selected_loan["emidetails"][emi_key] = emi_amt

            try:
                with open("loan_details.json","r") as jr:
                    loan_details = json.load(jr)
            except (FileNotFoundError, json.JSONDecodeError):
                print("\nSomething went wrong, please try again later.\n")
                return

            accno_key = str(self._account_number)
            if accno_key in loan_details and len(loan_details[accno_key]) > loan_index:
                loan_details[accno_key][loan_index] = selected_loan
            else:
                print("\nUnable to update loan details, please try again later.\n")
                return None

            with open("loan_details.json","w") as jw:
                json.dump(loan_details, jw, indent=4)

            self._balance_user -= emi_amount
            Loan._capital_bank += emi_amount
            Loan.update_bank_capital()
            transaction = self.format_transaction(emi_amount, f"{selected_loan.get('type', 'Loan')} EMI")
            self.update_amount(transaction)
            print("\nEMI paid successfully.\n")
        except InsufficientFund:
            print(f"\nInsufficient funds! Your current balance is {self._balance_user} but EMI amount is {emi_amount}.\n")

    def view_loans(self):
        if self._is_valid_user == False:
            self.login_error()
            return None

        self.fetch_loans()
        if not self._loans:
            print("\nYou have no active loans.\n")
            return None

        print("")
        for counter, loan in enumerate(self._loans, start=1):
            paid_emis = len(loan.get("emidetails", {}))
            duration = loan.get("duration")
            remaining = None
            if isinstance(duration, int):
                remaining = max(duration - paid_emis, 0)
            print(
                f"{counter} - {loan.get('type', 'Loan')} | Amount: {loan.get('amount')} | "
                f"EMI: {loan.get('emiamount')} | Duration: {duration} | "
                f"Paid EMIs: {paid_emis} | Remaining: {remaining}"
            )

class Combined(Loan):
    _is_valid_user = False

    def __init__(self):
        super().__init__()
        self._is_valid_user = super()._is_valid_user

    def validity(self):
        return self._is_valid_user
    

def loan_display(user):
    
    try:
        fname, lname, accno = user.fetch_details()
    except TypeError:
        fname, lname, accno = "","",0
    
    while True:
        print(f"""
\nWelcome! {fname} {lname}
Account Number : {accno}
--------- Select your choice ------------
1. Take a loan
2. Pay EMI
3. View your loans
4. Go back to main menu
""")
        
        try:
            loan_choice_raw = input("\nPlease enter your choice (or 'q' to quit) : ").strip().lower()
            if loan_choice_raw == "q":
                return None
            loan_choice = int(loan_choice_raw)
            if loan_choice < 1 or loan_choice > 4:
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid choice.")
            continue

        match loan_choice:
            case 1:
                user.take_loan()
            case 2:
                user.pay_emi()
            case 3:
                user.view_loans()
            case 4:
                return None
            case _:
                print("\nPlease enter a valid input.")

def transactions_display(user):
    
    try:
        fname, lname, accno = user.fetch_details()
    except TypeError:
        fname, lname, accno = "","",0

    while True:
        print(f"""
\nWelcome! {fname} {lname}
Account Number : {accno}
--------- Select your choice ----------
1. Deposite Money
2. Withdraw Money
3. Loan Options
4. Change your password
5. Logout
""")

        try:
            transaction_choice_raw = input("\nPlease enter your choice (or 'q' to quit) : ").strip().lower()
            if transaction_choice_raw == "q":
                user.logout()
                return None
            transaction_choice = int(transaction_choice_raw)
            if transaction_choice < 1 or transaction_choice > 5:
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid choice.")
            continue

        match transaction_choice:
            case 1:
                user.deposite()
            case 2:
                user.withdraw()
            case 3:
                loan_display(user)
            case 4:
                user.change_password()
            case 5:
                user.logout()
                return None
            case _:
                print("\nPlease enter a valid input.")


def initialize_required_files():
    """Initialize all required JSON files with default structures if they don't exist."""
    
    required_files = {
        "account_credentials.json": {},
        "account_details.json": {},
        "bank_details.json": {
            "name": "Laxmi Chit Fund",
            "ifsc": "LXM101532353",
            "addr": "Powder Gali - Mumbai",
            "crrcapital": 0
        },
        "loan_details.json": {},
        "transactions.json": {}
    }
    
    for filename, default_content in required_files.items():
        if not os.path.exists(filename):
            try:
                with open(filename, "w") as f:
                    json.dump(default_content, f, indent=4)
                print(f"Created {filename} with default structure.")
            except Exception as e:
                print(f"Error creating {filename}: {e}")


def main():
    initialize_required_files()
    user = Combined()
    while True:
        print("""
\n--------- Welcome to the Bank ---------
1. Create your account
2. Login
3. Exit
    """)
        
        try:
            first_choice_raw = input("\nPlease enter your choice (or 'q' to quit) : ").strip().lower()
            if first_choice_raw == "q":
                break
            first_choice = int(first_choice_raw)
            if first_choice < 1 or first_choice > 3:
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid choice.")
            continue

        if first_choice == 1:
            user.create_account()
        elif first_choice == 2:
            user.login()
            if(user.validity()):
                transactions_display(user)
        elif first_choice == 3:
            break
        else:
            print("\nPlease enter a valid input.")

if __name__ == "__main__":
    main()