from datetime import datetime
import json
import os

class Account:
    def __init__(self, account_number, name, pin, balance=0, blocked=False, is_admin=False, transactions=None):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.blocked = blocked
        self.is_admin = is_admin
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
        if amount <= 0: return False, "Invalid Amount"
        self.balance += amount
        self.add_transaction("Deposit", amount, "ATM")
        return True, "Deposit Successful"

    def withdraw(self, amount):
        if amount <= 0: return False, "Invalid Amount"
        if amount > self.balance: return False, "Insufficient Balance"
        self.balance -= amount
        self.add_transaction("Withdraw", amount, "ATM")
        return True, "Withdraw Successful"

    def receive_transfer(self, amount, source_info):
        self.balance += amount
        self.add_transaction("Transfer In", amount, source_info)

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "blocked": self.blocked,
            "is_admin": self.is_admin,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["account_number"],
            data["name"],
            data["pin"],
            data["balance"],
            data.get("blocked", False),
            data.get("is_admin", False),
            data.get("transactions", [])
        )

class Bank:
    def __init__(self):
        self.accounts = {}
        self.data_file = "data.json"
        self.load_data()

    def save_data(self):
        data_to_save = {str(k): v.to_dict() for k, v in self.accounts.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def load_data(self):
        if not os.path.exists(self.data_file): return
        try:
            with open(self.data_file, 'r') as f:
                raw = json.load(f)
                for k, v in raw.items():
                    self.accounts[int(k)] = Account.from_dict(v)
        except: pass

    def create_account(self, name, pin, initial_balance=0, is_admin=False):
        new_id = max(self.accounts.keys()) + 1 if self.accounts else 1001
        new_acc = Account(new_id, name, pin, initial_balance, is_admin=is_admin)
        self.accounts[new_id] = new_acc
        self.save_data()
        return new_acc

    def user_login(self, account_number, pin):
        acc = self.accounts.get(account_number)
        if not acc: return False, "Account Not Found"
        if acc.blocked and not acc.is_admin: return False, "Account Blocked"
        if not acc.check_pin(pin): return False, "Wrong PIN"
        return True, acc

    def transfer(self, s_id, r_id, amount, pin):
        s, r = self.accounts.get(s_id), self.accounts.get(r_id)
        if not s or not s.check_pin(pin): return False, "Auth Failed"
        if not r or s_id == r_id or amount <= 0 or s.balance < amount:
            return False, "Transfer Invalid"
        s.balance -= amount
        s.add_transaction("Transfer Out", amount, f"To {r.name} #{r_id}")
        r.receive_transfer(amount, f"From {s.name} #{s_id}")
        self.save_data()
        return True, "Transfer Success"

    def reset_pin_with_security_answer(self, account_number, answer, new_pin):
        acc = self.accounts.get(account_number)
        if not acc: return False, "Account Not Found"
        if answer.strip().lower() in ["lirone_fitoussi"]:
            acc.pin = new_pin
            self.save_data()
            return True, "PIN Reset Success"
        return False, "Incorrect Security Answer"

    def get_all_accounts(self):
        return list(self.accounts.values())
