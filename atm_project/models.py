from datetime import datetime
import json
import os
class Account:
    def __init__(self, account_number, name, pin, balance=0, blocked=False, transactions=None):
        self.account_number = account_number 
        self.name = name
        self.pin = pin 
        self.balance = balance
        self.blocked = blocked
        self.transactions = transactions if transactions else [] # ose history shel ha transc , matil be empty im lo samim shum davar

    
    def check_pin(self, pin): # bodek im ha pin toem
        return self.pin == pin
    
    def add_transaction(self, t_type, amount, source=None):
        transaction = { #ose dict im kol ha pratim
            "type": t_type,
            "amount": amount,
            "source": source,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M") # roshem et ha zman ha meduyak she butza iska
        }
        self.transactions.append(transaction) # append this ^ to history list
    def deposit(self, amount):
        if amount <= 0: # bodek im mispar Positive im lo , not valid
            return False, "Not Vaild"
        
        self.balance += amount
        self.add_transaction("Deposit", amount) # ose log la transaction history
        return True, "Deposit Succsucfull"
    
    def withdraw(self, amount):
        if amount <= 0: # bodek she ha withdraw hegyoni ve lo minus
            return False, "Number Not Vaild"
        
        if amount > self.balance: # bodek im la acc have enough money lasot withdraw
            return False,"Not Enough Balance"
        
        self.balance -= amount # morid et ha acc balance
        self.add_transaction("Withdraw", amount) # ose le ze tiud
        return True, "Withdraw Sucsuccfull"
    
    def recive_transfer(self, amount, from_account):
        self.balance += amount
        self.add_transaction("trasfer_in", amount, from_account) # ose tiud

    def change_pin(self, old_pin, new_pin):
        if self.pin != old_pin: # bodek she ha acc/user yodea et ha pin shelo lifney she o meshane
            return False, "Old Pin Incoorect"
        
        self.pin = new_pin # ose update la pin im new value
        return True, "Pin Updated Succsucfully"
    
    def to_dict(self): # mahlif et acc obj le simple dict bishvil lismor ba json file
        return {
            "account_number": self.account_number,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "blocked": self.blocked,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["account_number"],
            data["name"],
            data["pin"],
            data["balance"],
            data["blocked"],
            data["transactions"]
        )

# acc = Account(123, "Eli", "1111")

# print(acc.deposit(200))
# print(acc.withdraw(60))
# print(acc.change_pin("1111", "2222"))

# print(acc.to_dict())
class Bank:
    def __init__(self):
        self.accounts = {} 
        self.data_file = "data.json" # Savind Data inside data.json
        self.admin_password = "admin" # pass for admin
        self.load_data() # First of all load the data from data.json

    def save_data(self): # Convert acc obj to simple dictionary
        data_to_save = {acc_id: acc.to_dict() for acc_id, acc in self.accounts.items()}
        with open(self.data_file, 'w') as f: # open data file in write mode
            json.dump(data_to_save, f, indent=4)


    def load_data(self): # Checking the data file to prevent crashing program
        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, 'r') as f:
            raw_data = json.load(f) 

            for acc_id, acc_info in raw_data.items():
                new_acc_obj = Account.from_dict(acc_info)
                self.accounts[int(acc_id)] = new_acc_obj # Storing the id in Integer

    def create_account(self, name, pin, initial_balance=0):
        new_id = max(self.accounts.keys()) +1 if self.accounts else 1001    # ose new id, mathl be 1001 ve mosif 1 kol paam           
        new_acc = Account(new_id, name, pin, initial_balance) # ose new acc im ma she yesh ba sograim
        self.accounts[new_id] = new_acc # shomer et ha new acc 
        self.save_data() # shomer ba disc she lo disaper shom davar
        return new_acc
    
    def admin_login(self,password):
        if password == self.admin_password: # bodek she ha sisma hi kmo she zarih
            return True, "Admin Access Aproved"
        return False, "Incorrect Admin Password"
    
    def user_login(self, account_number, pin):
        acc = self.accounts.get(account_number)
        if not acc: # bodek im acc exist ba storage
            return False, "Account Number Not found"
        if acc.blocked: # bodek im acc blocked
            return False, "This Account is Blocked"
        if not acc.check_pin(pin): # bodek im pin toem 
            return False, "Wrong Pin Number"
        return True, acc
    
    def transfer(self, sender_id, reciver_id, amount, pin): # bodek im sender kayam + pin nahon
        sender = self.accounts.get(sender_id)
        receiver = self.accounts.get(reciver_id)
        #BDIKA LIFNEY SHE NOGIM BA KESEF
        if not sender or not sender.check_pin(pin):
            return False, "Authentication Failed (PIN)"
        if not receiver: # bodek im yesh account kaze ba system
            return False, "We Didndet Found Target Account to send"
        if amount <= 0: # mehayev she amount mispar positive
            return False, "Ammount Cannot be Negative, Only Positive"
        success, message = sender.withdraw(amount)
        if not success:
            return False, message 
        
        receiver.recive_transfer(amount, f"From {sender.name} ({sender_id}") # if withdraw succedded, tase deposit la reciver acc
        sender.add_transaction("Transfer Out", amount, f"To {receiver.name}") # record la transaction 

        self.save_data() # save data untill now

        return True, f"Transferred {amount} to {receiver.name} Successfully!"
    
    def get_all_accounts(self): 
        return list(self.accounts.values()) # Convert all acc obj into list format for admin view
