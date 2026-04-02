from eror import eror_list
from datetime import datetime
history1 =[]
history2 =[]
history3 =[]
class Account:
    def __init__(self,name,account_id,pin,balance,active,transaction_history,admin_convictions):
        self.name = name
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.active = active
        self.transaction_history = transaction_history
        self.admin_convictions = admin_convictions
        
account1 = Account("michael",123456,1234,5000,True,history1,False)
account2 = Account("eli",838355,5678,15000,True,history2,False)
account3 = Account("GOD",111111,1818,100000,True,history3,True)
all_accounts = [account1, account2, account3]

def enter_pin():
    try:
     pin_input = int(input("enter pin: "))
    except:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        error_msg = f"[{now}] ERROR: User entered Letters, not numbers."
        eror_list.append(error_msg)
        

         
    