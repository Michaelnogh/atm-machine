import customtkinter as ctk
from tkinter import messagebox
from models import Bank, Account # the logic
import time

class ATMApp:
    def __init__(self, root, bank):
        self.root = root
        self.bank = bank
        self.current_user = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.title("Hello World Bank - Secure System")
        self.root.geometry("800x950")

        self.login_screen()

    
    def update_clock(self):
        now = time.strftime("%H:%M:%S  |  %d/%m/%Y")
        if hasattr(self, 'clock_label'):
            self.clock_label.configure(text=now)
        self.root.after(1000, self.update_clock) # 1000milisec = 1 sec

    def clear(self): #to change the screen from a to b
        for w in self.root.winfo_children(): 
            w.destroy() # removing button,txt
           
        f = ctk.CTkFrame(self.root, fg_color="transparent")
        f.pack(side="top", anchor="ne", padx=10, pady=5)
        ctk.CTkOptionMenu(f, values=["Dark", "Light"], command=ctk.set_appearance_mode, width=90).pack()
        
        self.clock_label = ctk.CTkLabel(
            self.root, 
            text="", 
            font=("Courier New", 22, "bold"), 
            text_color="#3498db" 
        )
        self.clock_label.pack(side="bottom", pady=30) 
        self.update_clock()

    # SECURITY FOR PIN (RESET PIN BUTTON)
    def forgot_pin(self):
        win = ctk.CTkToplevel(self.root)
        win.geometry("400x400"); win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="Reset PIN", font=("Arial", 18, "bold")).pack(pady=15)
        acc_e = ctk.CTkEntry(win, placeholder_text="Account #"); acc_e.pack(pady=5)
        ans_e = ctk.CTkEntry(win, placeholder_text="Favorite Lecturer?"); ans_e.pack(pady=5)
        pin_e = ctk.CTkEntry(win, placeholder_text="New PIN", show="*"); pin_e.pack(pady=5)
        res_l = ctk.CTkLabel(win, text=""); res_l.pack()
        
        def do_reset():
            try:
                #checking the bank to see if the secret answer correct
                s, m = self.bank.reset_pin_with_security_answer(int(acc_e.get()), ans_e.get(), pin_e.get())
                res_l.configure(text=m, text_color="green" if s else "red")
            except: 
                res_l.configure(text="Invalid Input", text_color="red")
        
        ctk.CTkButton(win, text="Reset", command=do_reset).pack(pady=15)

    # --- Admin/Logs ---
    def toggle_user(self, aid):
        self.bank.accounts[aid].blocked = not self.bank.accounts[aid].blocked
        self.bank.save_data()
        self.show_admin_list()

    def view_logs(self, aid):
        win = ctk.CTkToplevel(self.root); win.geometry("600x450"); win.attributes("-topmost", True)
        txt = ctk.CTkTextbox(win, font=("Courier New", 12))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        user = self.bank.accounts[aid]
        log_data = f"--- Audit Logs for {user.name} (#{aid}) ---\n"
        log_data += "-"*60 + "\n"
        for t in reversed(user.transactions):
            log_data += f"{t['date']} | {t['type']:<12} | ${t['amount']:<8} | {t.get('source', 'N/A')}\n"
        txt.insert("0.0", log_data); txt.configure(state="disabled")

    # --- UI Screens ---
    def login_screen(self):
        self.clear()
        ctk.CTkLabel(self.root, text="Hello World Bank", font=("Arial", 45, "bold")).pack(pady=50)
        acc_e = ctk.CTkEntry(self.root, placeholder_text="Account #", width=250, height=35); acc_e.pack(pady=10)
        pin_e = ctk.CTkEntry(self.root, placeholder_text="PIN", show="*", width=250, height=35); pin_e.pack(pady=10)
        err_l = ctk.CTkLabel(self.root, text=""); err_l.pack()
        
        def do_login(): # login logic (*)
            try:
                s, r = self.bank.user_login(int(acc_e.get()), pin_e.get())
                if s: 
                    self.current_user = r # saveing the current user
                    self.main_screen()
                else: 
                    err_l.configure(text=r, text_color="red")
            except: 
                err_l.configure(text="Numbers only!", text_color="red")
        
        ctk.CTkButton(self.root, text="Login", command=do_login, width=200, height=40).pack(pady=10)
        ctk.CTkButton(self.root, text="Forgot PIN?", fg_color="transparent", command=self.forgot_pin).pack()

    def main_screen(self):
        self.clear() # im ho admin - red , im ho user - light blue
        color = "#c0392b" if self.current_user.is_admin else "#2c3e50"
        header = ctk.CTkFrame(self.root, height=120, fg_color=color); header.pack(fill="x")
        ctk.CTkLabel(header, text=f"Hello, {self.current_user.name}", font=("Arial", 22, "bold")).pack(pady=10)
        
        self.bal_l = ctk.CTkLabel(header, text=f"Balance: ${self.current_user.balance:,.2f}", font=("Arial", 20, "bold"))
        self.bal_l.pack()

        if self.current_user.is_admin: # im ho admin 
            tabs = ctk.CTkTabview(self.root); tabs.pack(fill="both", expand=True, padx=20, pady=10)
            self.setup_personal(tabs.add("My Account"))
            self.setup_manage(tabs.add("Manage Users"))
            self.setup_create(tabs.add("New Account"))
        else: #Im ho user
            f = ctk.CTkFrame(self.root, fg_color="transparent"); f.pack(fill="both", expand=True)
            self.setup_personal(f)
        
        ctk.CTkButton(self.root, text="Logout", fg_color="red", command=self.login_screen).pack(pady=10)

    def setup_personal(self, frame):
        ctk.CTkLabel(frame, text="Quick Actions", font=("Arial", 18, "bold")).pack(pady=10)
        box = ctk.CTkFrame(frame, fg_color="transparent"); box.pack()
        ctk.CTkButton(box, text="Withdraw", width=100, command=lambda: self.show_act("W")).grid(row=0, column=0, padx=5)
        ctk.CTkButton(box, text="Deposit", width=100, command=lambda: self.show_act("D")).grid(row=0, column=1, padx=5)
        ctk.CTkButton(box, text="Transfer", width=100, command=lambda: self.show_act("T")).grid(row=0, column=2, padx=5)
        ctk.CTkButton(box, text="History", width=100, command=self.show_my_history).grid(row=0, column=3, padx=5)
        
        self.info_l = ctk.CTkLabel(frame, text=""); self.info_l.pack()
        self.dyn_f = ctk.CTkFrame(frame, height=250, fg_color="#34495e"); self.dyn_f.pack(fill="both", expand=True, padx=20, pady=10)

    def show_my_history(self):
        for w in self.dyn_f.winfo_children(): w.destroy()
        txt = ctk.CTkTextbox(self.dyn_f, font=("Courier New", 11))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        log_data = "Your Transactions:\n" + "-"*50 + "\n"
        for t in reversed(self.current_user.transactions):
            log_data += f"{t['date']} | {t['type']:<12} | ${t['amount']:<7} | {t.get('source', 'ATM')}\n"
        txt.insert("0.0", log_data)
        txt.configure(state="disabled")

    def show_act(self, mode):
        for w in self.dyn_f.winfo_children(): w.destroy()
        if mode in ["W", "D"]:
            e = ctk.CTkEntry(self.dyn_f, placeholder_text="Amount"); e.pack(pady=10)
            def run():
                try:
                    amt = float(e.get())
                    s, m = (self.current_user.withdraw(amt) if mode == "W" else self.current_user.deposit(amt))
                    if s: 
                        self.bank.save_data()
                        self.bal_l.configure(text=f"Balance: ${self.current_user.balance:,.2f}")
                        self.info_l.configure(text=m, text_color="green")
                    else: self.info_l.configure(text=m, text_color="red")
                except: self.info_l.configure(text="Invalid Amount", text_color="red")
            ctk.CTkButton(self.dyn_f, text="Confirm", command=run).pack()
        elif mode == "T":
            target = ctk.CTkEntry(self.dyn_f, placeholder_text="Target #"); target.pack(pady=5)
            amt_e = ctk.CTkEntry(self.dyn_f, placeholder_text="Amount"); amt_e.pack(pady=5)
            def run_t():
                try:
                    s, m = self.bank.transfer(self.current_user.account_number, int(target.get()), float(amt_e.get()), self.current_user.pin)
                    if s: 
                        self.bal_l.configure(text=f"Balance: ${self.current_user.balance:,.2f}")
                        self.info_l.configure(text=m, text_color="green")
                    else: self.info_l.configure(text=m, text_color="red")
                except: self.info_l.configure(text="Error", text_color="red")
            ctk.CTkButton(self.dyn_f, text="Transfer", command=run_t).pack()

    def setup_manage(self, frame):
        self.list_f = ctk.CTkScrollableFrame(frame); self.list_f.pack(fill="both", expand=True, padx=10, pady=10)
        self.show_admin_list()

    def show_admin_list(self):
        for w in self.list_f.winfo_children(): w.destroy()
        for acc in self.bank.get_all_accounts():
            r = ctk.CTkFrame(self.list_f); r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=f"{acc.name} (#{acc.account_number})", width=150).pack(side="left", padx=5)
            ctk.CTkButton(r, text="Log", width=50, command=lambda aid=acc.account_number: self.view_logs(aid)).pack(side="right", padx=2)
            if not acc.is_admin:
                t = "Unblock" if acc.blocked else "Block"
                c = "green" if acc.blocked else "red"
                ctk.CTkButton(r, text=t, fg_color=c, width=70, command=lambda aid=acc.account_number: self.toggle_user(aid)).pack(side="right", padx=2)

    def setup_create(self, frame):
        ctk.CTkLabel(frame, text="Create New User", font=("Arial", 16)).pack(pady=10)
        n = ctk.CTkEntry(frame, placeholder_text="Name"); n.pack(pady=5)
        p = ctk.CTkEntry(frame, placeholder_text="PIN"); p.pack(pady=5)
        b = ctk.CTkEntry(frame, placeholder_text="Initial Balance"); b.pack(pady=5)
        msg = ctk.CTkLabel(frame, text=""); msg.pack()
        def do_c():
            try:
                self.bank.create_account(n.get(), p.get(), float(b.get()))
                msg.configure(text="Created!", text_color="green"); self.show_admin_list()
            except: msg.configure(text="Error", text_color="red")
        ctk.CTkButton(frame, text="Create", command=do_c).pack(pady=10)

if __name__ == "__main__":
    main_bank = Bank()
    if not main_bank.accounts:
        main_bank.create_account("Admin", "1234", 1000, is_admin = True)

    root_window = ctk.CTk()
    app = ATMApp(root_window, main_bank)
    root_window.mainloop()