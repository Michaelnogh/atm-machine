from atm_project.models import Bank
def run_test():
    bank = Bank()
    print("---Starting bank test---")
# Checking with two acc
    acc1 = bank.create_account("Eli", "1111", 500)
    acc2 = bank.create_account("Yossi", "2222", 100)
    print(f"Created Account 1: {acc1.account_number} (Name: {acc1.name})")
    print(f"Created Account 2: {acc2.account_number} (Name: {acc2.name})")

    if acc1.account_number != acc2.account_number:
        print(" Success: Unique Account Numbers generated.")
    else:
        print(" Fail: Account numbers are the same!")

    success, message = bank.user_login(acc1.account_number, "9999") 
    if not success:
        print(f"success, login failed as expected. message: {message}")
    else:
        print("fail login should have failed with worng pin") 

    # check if you withdraw to acc not regiterd

    success, message = bank.transfer(acc1.account_number, 9999, 50, "1111")
    if not success and "Target Account Not Found" in message:
        print(f" Success: Transfer to non-existent account failed. Message: {message}")
    else:
        print(" Fail: Transfer should have failed for invalid target!")

#check if withdraw that succsueed
    old_balance_sender = acc1.balance
    old_balance_receiver = acc2.balance
    amount_to_transfer = 150              
    success, message = bank.transfer(acc1.account_number, acc2.account_number, amount_to_transfer, "1111")

    if success:
        print(f" Success: Transfer completed. Message: {message}")
        # checking if the money really geting down
        if acc1.balance == (old_balance_sender - amount_to_transfer) and \
           acc2.balance == (old_balance_receiver + amount_to_transfer):
            print(" Success: Balances updated correctly in both accounts.")
        else:
            print(" Fail: Balances were not updated correctly!")
    else:
        print(f" Fail: Transfer failed. Message: {message}")

if __name__ == "__main__":
    run_test()
