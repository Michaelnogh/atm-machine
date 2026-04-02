history = ["hu"]

class Account:
    def __init__(self,name,account_id,pin,balance,active_account,transaction_history):
        self.name = name
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.active_account = active_account
        self.transaction_history = transaction_history

account1 = Account("michel",123456,1234,50000,True,history1)
account2 = Account()


