from datetime import datetime
from storage import *
import json

class Account:
    def __init__(self,name,account_id,pin,balance,active,transaction_history,admin_convictions):
        self.name = name
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.active = active
        self.transaction_history = transaction_history
        self.admin_convictions = admin_convictions
        


def load_data():
    try:
        with open("accounts.json", "r") as f:
            # טעינת הרשימה מהקובץ
            data = json.load(f)
            
            # הפיכה של כל מילון ב-JSON לאובייקט Account
            all_accounts = []
            for item in data:
                acc = Account(
                    item["name"], 
                    item["account_id"], 
                    item["pin"], 
                    item["balance"], 
                    item["active"], 
                    item["transaction_history"], 
                    item["admin_convictions"]
                )
                all_accounts.append(acc)
            return all_accounts
    except FileNotFoundError:
        print("קובץ הנתונים לא נמצא!")
        return []

def save_data(all_accounts):
    # הפיכת כל האובייקטים חזרה למילונים פשוטים
    data_to_save = []
    for acc in all_accounts:
        data_to_save.append({
            "name": acc.name,
            "account_id": acc.account_id,
            "pin": acc.pin,
            "balance": acc.balance,
            "active": acc.active,
            "transaction_history": acc.transaction_history,
            "admin_convictions": acc.admin_convictions
        })
    
    # כתיבה לקובץ
    with open("accounts.json", "w") as f:
        json.dump(data_to_save, f, indent=4)

         
    