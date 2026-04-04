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
        self.transactions = transactions if transactions else []

    
    def check_pin(self, pin):
        return self.pin == pin
    
    def add_transaction(self, t_type, amount, source=None):
        transaction = {
            "type": t_type,
            "amount": amount,
            "source": source,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.transactions.append(transaction)
    def deposit(self, amount):
        if amount <= 0:
            return False, "Not Vaild"
        
        self.balance += amount
        self.add_transaction("Deposit", amount)
        return True, "Deposit Succsucfull"
    
    def withdraw(self, amount):
        if amount <= 0:
            return False, "Number Not Vaild"
        
        if amount > self.balance:
            return False,"Not Enough Balance"
        
        self.balance -= amount
        self.add_transaction("Withdraw", amount)

        return True, "Withdraw Sucsuccfull"
    
    def recive_transfer(self, amount, from_account):
        self.balance += amount
        self.add_transaction("trasfer_in", amount, from_account)

    def change_pin(self, old_pin, new_pin):
        if self.pin != old_pin:
            return False, "Old Pin Incoorect"
        
        self.pin = new_pin
        return True, "Pin Updated Succsucfully"
    
    def to_dict(self):
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
        self.account = {}
        self.data_file = "data.json"
        self.admin_password = "admin"
        self.load_data()

    def save_data(self):
        data_to_save = {acc_id: acc.to_dict() for acc_id, acc in self.accounts.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)


    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, 'r') as f:
            raw_data = json.load(f) 

            for acc_id, acc_info in raw_data.items():
                new_acc_obj = Account.from_dict(acc_info)
                self.accounts[int(acc_id)] = new_acc_obj

    def create_account(self, name, pin, initial_balance=0):
        new_id = max(self.account.keys()) +1 if self.accounts else 1001               
        new_acc = Account(new_id, name, pin, initial_balance)
        self.accounts[new_id] = new_acc
        self.save_data()
        return new_acc
    
    def admin_login(self,password):
        if password == self.admin_password:
            return True, "Admin Access Aproved"
        return False, "Incorrect Admin Password"
    
    def user_login(self, account_number, pin):
        acc = self.accounts.get(account_number)
        if not acc:
            return False, "Account Number Not found"
        if acc.blocked:
            return False, "This Account is Blocked"
        if not acc.check_pin(pin):
            return False, "Wrong Pin Number"
        return True, acc
    
    def transfer(self, sender_id, reciver_id, amount, pin):
        sender = self.accounts.get(sender_id)
        receiver = self.accounts.get(reciver_id)
        #BDIKA LIFNEY SHE NOGIM BA KESEF
        if not sender or not sender.check_pin(pin):
            return False, "Authentication Failed (PIN)"
        if not receiver:
            return False, "We Didndet Found Target Account to send"
        if amount <= 0:
            return False, "Ammount Cannot be Negative, Only Positive"
        success, message = sender.withdraw(amount)
        if not success:
            return False, message 
        
        receiver.recive_transfer(amount, f"From {sender.name} ({sender_id}")
        sender.add_transaction("Transfer Out", amount, f"To {receiver.name}")

        self.save_data()

        return True, f"Transferred {amount} to {receiver.name} Successfully!"
    
    def get_all_accounts(self):
        return list(self.accounts.values())
    