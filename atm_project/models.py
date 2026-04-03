from datetime import datetime
import json


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
    
    def add_transaction(self, t_type, ammount, source=None):
        transaction = {
            "type": t_type,
            "ammount": ammount,
            "source": source,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

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
    


acc = Account(123, "Eli", "1111")

print(acc.deposit(200))
print(acc.withdraw(50))
print(acc.change_pin("1111", "2222"))

