import customtkinter as ctk
from models import Bank  # מייבאים את המחלקה מהקובץ ששלחת

# --- הגדרות עיצוב ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- אתחול המערכת ---
# ברגע שאתה יוצר מופע של Bank, הוא מפעיל את self.load_data() אוטומטית
my_bank = Bank()

root = ctk.CTk()
root.title("DevOps Bank ATM")
root.geometry("500x550")

def login_action():
    """הפונקציה שמתחברת ללוגיקה של ה-Bank שכתבת"""
    acc_num_raw = acc_entry.get()
    pin = pin_entry.get()

    # בדיקה שהשדות לא ריקים
    if not acc_num_raw or not pin:
        label_status.configure(text="יש למלא את כל השדות", text_color="orange")
        return

    try:
        # המרה למספר (הבנק שלך מצפה ל-int)
        acc_num = int(acc_num_raw)
        
        # שימוש במתודה user_login מתוך models.py
        # היא מחזירה (True, acc_obj) או (False, "error message")
        success, result = my_bank.user_login(acc_num, pin)

        if success:
            # result הוא אובייקט ה-Account של המשתמש
            label_status.configure(text=f"ברוך הבא, {result.name}!", text_color="#2ecc71")
            print(f"התחברות הצליחה עבור חשבון: {acc_num}")
            
            # כאן בשלב הבא נוכל להוסיף פונקציה שתנקה את המסך ותציג תפריט
        else:
            # result הוא הודעת השגיאה שכתבת (למשל: "Wrong Pin Number")
            label_status.configure(text=result, text_color="#e74c3c")

    except ValueError:
        label_status.configure(text="מספר חשבון חייב להכיל ספרות בלבד", text_color="#e74c3c")

# --- בניית הממשק (Widgets) ---

# כותרת הבנק
bank_title = ctk.CTkLabel(root, text="DevOps Bank", font=("Segoe UI", 42, "bold"))
bank_title.pack(pady=(60, 30))

# שדה מספר חשבון
acc_entry = ctk.CTkEntry(root, placeholder_text="Account Number", width=300, height=45)
acc_entry.pack(pady=10)

# שדה סיסמה מוסתר
pin_entry = ctk.CTkEntry(root, placeholder_text="PIN Code", show="*", width=300, height=45)
pin_entry.pack(pady=10)

# כפתור התחברות שמפעיל את login_action
login_btn = ctk.CTkButton(root, text="התחבר", command=login_action, width=200, height=50, font=("Arial", 16, "bold"))
login_btn.pack(pady=30)

# הודעת סטטוס להצגת הצלחה או שגיאה
label_status = ctk.CTkLabel(root, text="", font=("Arial", 14))
label_status.pack(pady=10)

# הפעלת הלולאה הראשית של ה-UI
root.mainloop()