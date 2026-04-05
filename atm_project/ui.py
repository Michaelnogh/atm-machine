import customtkinter as ctk
from models import Bank, Account

# --- Init ---
my_bank = Bank()
if not my_bank.accounts:
    my_bank.create_account("Admin", "1234", 1000, is_admin=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("DevOps Bank System")
root.geometry("800x900")
current_user = None

def change_theme(mode): ctk.set_appearance_mode(mode)

def clear():
    for w in root.winfo_children(): w.destroy()
    f = ctk.CTkFrame(root, fg_color="transparent")
    f.pack(side="top", anchor="ne", padx=10, pady=5)
    ctk.CTkOptionMenu(f, values=["Dark", "Light"], command=change_theme, width=90).pack()

# --- Security ---
def forgot_pin():
    win = ctk.CTkToplevel(root)
    win.geometry("400x400"); win.attributes("-topmost", True)
    ctk.CTkLabel(win, text="Reset PIN", font=("Arial", 18, "bold")).pack(pady=15)
    acc_e = ctk.CTkEntry(win, placeholder_text="Account #"); acc_e.pack(pady=5)
    ans_e = ctk.CTkEntry(win, placeholder_text="Favorite Lecturer?"); ans_e.pack(pady=5)
    pin_e = ctk.CTkEntry(win, placeholder_text="New PIN", show="*"); pin_e.pack(pady=5)
    res_l = ctk.CTkLabel(win, text=""); res_l.pack()
    def do_reset():
        try:
            s, m = my_bank.reset_pin_with_security_answer(int(acc_e.get()), ans_e.get(), pin_e.get())
            res_l.configure(text=m, text_color="green" if s else "red")
        except: res_l.configure(text="Invalid Input", text_color="red")
    ctk.CTkButton(win, text="Reset", command=do_reset).pack(pady=15)

# --- Admin/Logs ---
def toggle_user(aid):
    my_bank.accounts[aid].blocked = not my_bank.accounts[aid].blocked
    my_bank.save_data(); show_admin_list()

def view_logs(aid):
    win = ctk.CTkToplevel(root); win.geometry("600x450"); win.attributes("-topmost", True)
    txt = ctk.CTkTextbox(win, font=("Courier New", 12))
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    user = my_bank.accounts[aid]
    log_data = f"--- Audit Logs for {user.name} (#{aid}) ---\n"
    log_data += "-"*60 + "\n"
    for t in reversed(user.transactions):
        # כאן הוספנו את ה-source לאדמין
        log_data += f"{t['date']} | {t['type']:<12} | ${t['amount']:<8} | {t.get('source', 'N/A')}\n"
    txt.insert("0.0", log_data); txt.configure(state="disabled")

# --- UI Screens ---
def login_screen():
    clear()
    ctk.CTkLabel(root, text="DevOps Bank", font=("Arial", 40, "bold")).pack(pady=50)
    acc_e = ctk.CTkEntry(root, placeholder_text="Account #"); acc_e.pack(pady=10)
    pin_e = ctk.CTkEntry(root, placeholder_text="PIN", show="*"); pin_e.pack(pady=10)
    err_l = ctk.CTkLabel(root, text=""); err_l.pack()
    def do_login():
        global current_user
        try:
            s, r = my_bank.user_login(int(acc_e.get()), pin_e.get())
            if s: current_user = r; main_screen()
            else: err_l.configure(text=r, text_color="red")
        except: err_l.configure(text="Numbers only!", text_color="red")
    ctk.CTkButton(root, text="Login", command=do_login).pack(pady=10)
    ctk.CTkButton(root, text="Forgot PIN?", fg_color="transparent", command=forgot_pin).pack()

def main_screen():
    clear()
    color = "#c0392b" if current_user.is_admin else "#2c3e50"
    header = ctk.CTkFrame(root, height=100, fg_color=color); header.pack(fill="x")
    ctk.CTkLabel(header, text=f"Hello, {current_user.name}", font=("Arial", 20)).pack(pady=10)
    global bal_l
    bal_l = ctk.CTkLabel(header, text=f"Balance: ${current_user.balance:,.2f}", font=("Arial", 18, "bold")); bal_l.pack()

    if current_user.is_admin:
        tabs = ctk.CTkTabview(root); tabs.pack(fill="both", expand=True, padx=20, pady=10)
        setup_personal(tabs.add("My Account"))
        setup_manage(tabs.add("Manage Users"))
        setup_create(tabs.add("New Account"))
    else:
        f = ctk.CTkFrame(root, fg_color="transparent"); f.pack(fill="both", expand=True)
        setup_personal(f)
    ctk.CTkButton(root, text="Logout", fg_color="red", command=login_screen).pack(pady=10)

def setup_personal(frame):
    global dyn_f, info_l
    ctk.CTkLabel(frame, text="Quick Actions", font=("Arial", 16, "bold")).pack(pady=10)
    box = ctk.CTkFrame(frame, fg_color="transparent"); box.pack()
    ctk.CTkButton(box, text="Withdraw", width=90, command=lambda: show_act("W")).grid(row=0, column=0, padx=2)
    ctk.CTkButton(box, text="Deposit", width=90, command=lambda: show_act("D")).grid(row=0, column=1, padx=2)
    ctk.CTkButton(box, text="Transfer", width=90, command=lambda: show_act("T")).grid(row=0, column=2, padx=2)
    ctk.CTkButton(box, text="History", width=90, command=show_my_history).grid(row=0, column=3, padx=2)
    
    info_l = ctk.CTkLabel(frame, text=""); info_l.pack()
    dyn_f = ctk.CTkFrame(frame, height=200, fg_color="#34495e"); dyn_f.pack(fill="both", expand=True, padx=20, pady=10)

def show_my_history():
    for w in dyn_f.winfo_children(): w.destroy()
    txt = ctk.CTkTextbox(dyn_f, font=("Courier New", 11))
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    log_data = "Your Transactions:\n" + "-"*50 + "\n"
    for t in reversed(current_user.transactions):
        # כאן הוספנו את ה-source למשתמש הרגיל
        log_data += f"{t['date']} | {t['type']:<12} | ${t['amount']:<7} | {t.get('source', 'ATM')}\n"
    txt.insert("0.0", log_data)
    txt.configure(state="disabled")

def show_act(mode):
    for w in dyn_f.winfo_children(): w.destroy()
    if mode in ["W", "D"]:
        e = ctk.CTkEntry(dyn_f, placeholder_text="Amount"); e.pack(pady=10)
        def run():
            try:
                amt = float(e.get())
                s, m = (current_user.withdraw(amt) if mode == "W" else current_user.deposit(amt))
                if s: 
                    my_bank.save_data()
                    bal_l.configure(text=f"Balance: ${current_user.balance:,.2f}")
                    info_l.configure(text=m, text_color="green")
                else: info_l.configure(text=m, text_color="red")
            except: info_l.configure(text="Invalid Amount", text_color="red")
        ctk.CTkButton(dyn_f, text="Confirm", command=run).pack()
    elif mode == "T":
        target = ctk.CTkEntry(dyn_f, placeholder_text="Target #"); target.pack(pady=5)
        amt_e = ctk.CTkEntry(dyn_f, placeholder_text="Amount"); amt_e.pack(pady=5)
        def run_t():
            try:
                s, m = my_bank.transfer(current_user.account_number, int(target.get()), float(amt_e.get()), current_user.pin)
                if s: 
                    bal_l.configure(text=f"Balance: ${current_user.balance:,.2f}")
                    info_l.configure(text=m, text_color="green")
                else: info_l.configure(text=m, text_color="red")
            except: info_l.configure(text="Error", text_color="red")
        ctk.CTkButton(dyn_f, text="Transfer", command=run_t).pack()

def setup_manage(frame):
    global list_f; list_f = ctk.CTkScrollableFrame(frame); list_f.pack(fill="both", expand=True, padx=10, pady=10)
    show_admin_list()

def show_admin_list():
    for w in list_f.winfo_children(): w.destroy()
    for acc in my_bank.get_all_accounts():
        r = ctk.CTkFrame(list_f); r.pack(fill="x", pady=2)
        ctk.CTkLabel(r, text=f"{acc.name} (#{acc.account_number})", width=150).pack(side="left", padx=5)
        ctk.CTkButton(r, text="Log", width=50, command=lambda aid=acc.account_number: view_logs(aid)).pack(side="right", padx=2)
        if not acc.is_admin:
            t = "Unblock" if acc.blocked else "Block"
            c = "green" if acc.blocked else "red"
            ctk.CTkButton(r, text=t, fg_color=c, width=70, command=lambda aid=acc.account_number: toggle_user(aid)).pack(side="right", padx=2)

def setup_create(frame):
    ctk.CTkLabel(frame, text="Create New User", font=("Arial", 16)).pack(pady=10)
    n = ctk.CTkEntry(frame, placeholder_text="Name"); n.pack(pady=5)
    p = ctk.CTkEntry(frame, placeholder_text="PIN"); p.pack(pady=5)
    b = ctk.CTkEntry(frame, placeholder_text="Initial Balance"); b.pack(pady=5)
    msg = ctk.CTkLabel(frame, text=""); msg.pack()
    def do_c():
        try:
            my_bank.create_account(n.get(), p.get(), float(b.get()))
            msg.configure(text="Created!", text_color="green"); show_admin_list()
        except: msg.configure(text="Error", text_color="red")
    ctk.CTkButton(frame, text="Create", command=do_c).pack(pady=10)

login_screen()
root.mainloop()