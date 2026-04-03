# import random

# class Bank:
#     def __init__(self):
#         self.account = {}
#         self.admin_pin = "4321"

#     def create_account(self, owner_name, pin, initial_balance = 0):
#         while True:
#             acc_num = str(random.randint(10000, 99999))
#             if acc_num not in self.acoouns:
#                 break

#         new_account = Account(acc_num, owner_name, pin, initial_balance)

#         self.account[acc_num] = new_account
#         return acc_num
    
#     def get_account(self, account_number):
#         return self.account.get(account_number)
    
#     def authenticate_user(self, acoount_number, pin):
#         account = self.get_account(account_number)
        

class Account:
    def __init__(self,account_id, name,  ):
        pass       