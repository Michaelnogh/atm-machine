import customtkinter as ctk
from models import Bank, Account
import datetime

# --- הגדרות בנק ומראה ---
my_bank = Bank()
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("DevOps Global Bank - Secure System")
root.geometry("800x950")

current_user = None

# --- פונקציות תצוגה (Theme) ---
def change_appearance_mode(new_mode):
    ctk.set_appearance_mode(new_mode)

def add_theme_selector(parent):
    theme_frame = ctk.CTkFrame(parent, fg_color="transparent")
    theme_frame.pack(side="top", anchor="ne", padx=10, pady=5)
    
    ctk.CTkLabel(theme_frame, text="Theme:", font=("Arial", 11)).pack(side="left", padx=5)
    theme_menu = ctk.CTkOptionMenu(
        theme_frame, 
        values=["Dark", "Light", "System"],
        command=change_appearance_mode,
        width=100, height=25
    )
    theme_menu.pack(side="left")
    theme_menu.set("Dark")

# --- פונקציות עזר למסך ---
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()
    add_theme_selector(root)

def update_balance_display():
    if current_user:
        balance_label.configure(text=f"Current Balance: ${current_user.balance:,.2f}")

# --- מנגנון שחזור סיסמה (מבחוץ) ---
def forgot_pin_window():
    forgot_win = ctk.CTkToplevel(root)
    forgot_win.title("PIN Recovery")
    forgot_win.geometry("400x450")
    forgot_win.attributes("-topmost", True)

    ctk.CTkLabel(forgot_win, text="Reset Your PIN", font=("Arial", 20, "bold")).pack(pady=20)
    
    acc_entry = ctk.CTkEntry(forgot_win, placeholder_text="Account Number", width=250)
    acc_entry.pack(pady=10)

    ctk.CTkLabel(forgot_win, text="Security Question:\nWho is your favorite teacher?", font=("Arial", 13)).pack(pady=5)
    answer_entry = ctk.CTkEntry(forgot_win, placeholder_text="Enter Answer", width=250)
    answer_entry.pack(pady=10)

    new_pin_entry_field = ctk.CTkEntry(forgot_win, placeholder_text="New PIN", show="*", width=250)
    new_pin_entry_field.pack(pady=10)

    res_label = ctk.CTkLabel(forgot_win, text="")
    res_label.pack(pady=5)

    def attempt_reset():
        try:
            a_num = int(acc_entry.get())
            ans = answer_entry.get()
            n_pin = new_pin_entry_field.get()
            
            if not n_pin:
                res_label.configure(text="Enter a new PIN", text_color="red")
                return

            success, msg = my_bank.reset_pin_with_security_answer(a_num, ans, n_pin)
            if success:
                res_label.configure(text=msg, text_color="#2ecc71")
                forgot_win.after(2000, forgot_win.destroy)
            else:
                res_label.configure(text=msg, text_color="#e74c3c")
        except:
            res_label.configure(text="Invalid Input", text_color="#e74c3c")

    ctk.CTkButton(forgot_win, text="Update PIN", command=attempt_reset, fg_color="#27ae60").pack(pady=20)

# --- לוגיקה ניהולית ---
def toggle_status(aid):
    my_bank.accounts[aid].blocked = not my_bank.accounts[aid].blocked
    my_bank.save_data()
    show_admin_users_list()

def view_any_user_history(aid):
    user = my_bank.accounts[aid]
    history_win = ctk.CTkToplevel(root)
    history_win.title(f"Logs: {user.name}")
    history_win.geometry("600x400")
    history_win.attributes("-topmost", True)
    
    box = ctk.CTkTextbox(history_win, font=("Courier New", 12))
    box.pack(fill="both", expand=True, padx=20, pady=20)
    
    log = f"--- Audit Log for {user.name} (#{aid}) ---\n\n"
    if not user.transactions:
        log += "No transactions found."
    else:
        for t in reversed(user.transactions):
            log += f"{t.get('date')[:16]} | {t.get('type'):<12} | ${t.get('amount'):<8} | {t.get('source')}\n"
    
    box.insert("0.0", log)
    box.configure(state="disabled")

def execute_create_user():
    name = new_name_entry.get()
    pin = new_pin_entry.get()
    try:
        balance = float(new_balance_entry.get())
        if name and pin:
            new_acc = my_bank.create_account(name, pin, balance)
            admin_info_label.configure(text=f"Created Account #{new_acc.account_number}", text_color="#2ecc71")
            show_admin_users_list()
        else: admin_info_label.configure(text="Missing fields", text_color="#e74c3c")
    except: admin_info_label.configure(text="Invalid balance", text_color="#e74c3c")

# --- לוגיקה בנקאית ---
def execute_transfer_ui():
    try:
        t_id = int(target_acc_entry.get())
        amount = float(transfer_amount_entry.get())
        success, msg = my_bank.transfer(current_user.account_number, t_id, amount, current_user.pin)
        if success:
            update_balance_display()
            label_info.configure(text=msg, text_color="#2ecc71")
        else: label_info.configure(text=msg, text_color="#e74c3c")
    except: label_info.configure(text="Invalid Input", text_color="#e74c3c")

def common_action(mode):
    try:
        amount = float(action_entry.get())
        if mode == "W":
            success, msg = current_user.withdraw(amount)
        else:
            success, msg = current_user.deposit(amount)
        
        if success:
            my_bank.save_data()
            update_balance_display()
            label_info.configure(text=msg, text_color="#2ecc71")
        else: label_info.configure(text=msg, text_color="#e74c3c")
    except: label_info.configure(text="Invalid Amount", text_color="#e74c3c")

# --- מסכים וממשק ---
def setup_login_screen():
    clear_screen()
    ctk.CTkLabel(root, text="DevOps Bank", font=("Segoe UI", 45, "bold")).pack(pady=(50, 40))
    
    global acc_input, pin_input, label_error
    acc_input = ctk.CTkEntry(root, placeholder_text="Account Number", width=280, height=40)
    acc_input.pack(pady=10)
    pin_input = ctk.CTkEntry(root, placeholder_text="PIN Code", show="*", width=280, height=40)
    pin_input.pack(pady=10)
    
    ctk.CTkButton(root, text="Login", command=handle_login, width=200, height=45).pack(pady=15)
    ctk.CTkButton(root, text="Forgot PIN?", fg_color="transparent", text_color="#3498db", command=forgot_pin_window).pack()
    
    label_error = ctk.CTkLabel(root, text="")
    label_error.pack(pady=10)

def handle_login():
    global current_user
    try:
        acc_num = int(acc_input.get())
        pin = pin_input.get()
        success, result = my_bank.user_login(acc_num, pin)
        if success:
            current_user = result
            show_main_interface()
        else: label_error.configure(text=result, text_color="#e74c3c")
    except: label_error.configure(text="Please enter numbers only", text_color="#e74c3c")

def show_main_interface():
    clear_screen()
    color = "#c0392b" if current_user.is_admin else "#2c3e50"
    header = ctk.CTkFrame(root, height=120, fg_color=color)
    header.pack(fill="x")
    
    ctk.CTkLabel(header, text=f"Welcome, {current_user.name}", font=("Arial", 22, "bold")).pack(pady=(15, 5))
    global balance_label
    balance_label = ctk.CTkLabel(header, text="", font=("Arial", 20))
    balance_label.pack(pady=5)
    update_balance_display()

    if current_user.is_admin:
        tabview = ctk.CTkTabview(root)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        setup_personal_tab(tabview.add("My Account"))
        setup_manage_tab(tabview.add("Manage Users"))
        setup_create_tab(tabview.add("Create Account"))
    else:
        f = ctk.CTkFrame(root, fg_color="transparent")
        f.pack(fill="both", expand=True)
        setup_personal_tab(f)

    ctk.CTkButton(root, text="Logout", fg_color="#e74c3c", command=setup_login_screen).pack(pady=20)

def setup_personal_tab(frame):
    global label_info, dynamic_area
    ctk.CTkLabel(frame, text="Bank Services", font=("Arial", 18, "bold")).pack(pady=10)
    
    btn_box = ctk.CTkFrame(frame, fg_color="transparent")
    btn_box.pack(pady=10)
    ctk.CTkButton(btn_box, text="Withdraw", width=100, command=lambda: show_op("W")).grid(row=0, column=0, padx=5)
    ctk.CTkButton(btn_box, text="Deposit", width=100, command=lambda: show_op("D")).grid(row=0, column=1, padx=5)
    ctk.CTkButton(btn_box, text="Transfer", width=100, command=lambda: show_op("T")).grid(row=0, column=2, padx=5)
    ctk.CTkButton(btn_box, text="History", width=100, command=show_my_history).grid(row=0, column=3, padx=5)
    
    label_info = ctk.CTkLabel(frame, text="")
    label_info.pack(pady=5)
    
    dynamic_area = ctk.CTkFrame(frame, height=250, fg_color="#34495e")
    dynamic_area.pack(fill="both", expand=True, padx=30, pady=10)

def show_op(mode):
    for widget in dynamic_area.winfo_children(): widget.destroy()
    global action_entry, target_acc_entry, transfer_amount_entry
    
    if mode in ["W", "D"]:
        placeholder = "Withdraw Amount" if mode == "W" else "Deposit Amount"
        action_entry = ctk.CTkEntry(dynamic_area, placeholder_text=placeholder, width=200)
        action_entry.pack(pady=20)
        ctk.CTkButton(dynamic_area, text="Confirm", command=lambda: common_action(mode)).pack()
    elif mode == "T":
        target_acc_entry = ctk.CTkEntry(dynamic_area, placeholder_text="Target ID")
        target_acc_entry.pack(pady=5)
        transfer_amount_entry = ctk.CTkEntry(dynamic_area, placeholder_text="Amount")
        transfer_amount_entry.pack(pady=5)
        ctk.CTkButton(dynamic_area, text="Send Transfer", command=execute_transfer_ui).pack(pady=10)

def show_my_history():
    for widget in dynamic_area.winfo_children(): widget.destroy()
    box = ctk.CTkTextbox(dynamic_area)
    box.pack(fill="both", expand=True)
    log = "Your Transactions:\n" + "-"*40 + "\n"
    for t in reversed(current_user.transactions):
        log += f"{t.get('date')[:16]} | {t.get('type'):<12} | ${t.get('amount'):<7} | {t.get('source')}\n"
    box.insert("0.0", log)
    box.configure(state="disabled")

def setup_manage_tab(frame):
    global users_list_frame
    users_list_frame = ctk.CTkScrollableFrame(frame, height=450)
    users_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
    show_admin_users_list()

def show_admin_users_list():
    for widget in users_list_frame.winfo_children(): widget.destroy()
    for acc in my_bank.get_all_accounts():
        row = ctk.CTkFrame(users_list_frame)
        row.pack(fill="x", pady=2, padx=5)
        
        status_clr = "#e74c3c" if acc.blocked else "#2ecc71"
        ctk.CTkLabel(row, text=f"{acc.name} (#{acc.account_number})", width=180, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(row, text="●", text_color=status_clr).pack(side="left", padx=5)
        
        ctk.CTkButton(row, text="Log", width=50, command=lambda aid=acc.account_number: view_any_user_history(aid)).pack(side="right", padx=5)
        if not acc.is_admin:
            txt = "Unblock" if acc.blocked else "Block"
            clr = "#27ae60" if acc.blocked else "#c0392b"
            ctk.CTkButton(row, text=txt, width=75, fg_color=clr, command=lambda aid=acc.account_number: toggle_status(aid)).pack(side="right", padx=2)

def setup_create_tab(frame):
    global new_name_entry, new_pin_entry, new_balance_entry, admin_info_label
    ctk.CTkLabel(frame, text="Onboard New Client", font=("Arial", 18, "bold")).pack(pady=20)
    new_name_entry = ctk.CTkEntry(frame, placeholder_text="Full Name", width=300); new_name_entry.pack(pady=5)
    new_pin_entry = ctk.CTkEntry(frame, placeholder_text="Initial PIN", width=300); new_pin_entry.pack(pady=5)
    new_balance_entry = ctk.CTkEntry(frame, placeholder_text="Opening Balance", width=300); new_balance_entry.pack(pady=5)
    ctk.CTkButton(frame, text="Register Account", fg_color="#27ae60", command=execute_create_user).pack(pady=25)
    admin_info_label = ctk.CTkLabel(frame, text="")
    admin_info_label.pack()

# --- התחלת אפליקציה ---
setup_login_screen()
root.mainloop()