import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
from deep_translator import GoogleTranslator
import random
import speech_recognition as sr
import threading
from PIL import Image, ImageTk, ImageSequence
import mysql.connector
from datetime import datetime

# ------------------------ Database Configuration ------------------------ #
DB_CONFIG = {
    'user': 'root',
    'password': '0747',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'PythonTranslator'
}

# Global variables to manage scheduled tasks
bg_color_job = None
footer_style_job = None

# ------------------------ Root Window Setup ------------------------ #
root = tk.Tk()
root.withdraw()  # Hide the main window initially (will be shown after splash screen)

# ------------------------ Prompt User for Name ------------------------ #
user_name = simpledialog.askstring("User Input", "Please enter your name:")
if not user_name:
    exit()

# ------------------------ Log User Login Info into MySQL ------------------------ #
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    login_time = datetime.now()
    cursor.execute("INSERT INTO login_info (username, login_time) VALUES (%s, %s)", (user_name, login_time))
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print("Database Error:", e)

# ------------------------ Splash Screen Function ------------------------ #
def show_splash():
    splash_root = tk.Toplevel()
    splash_root.overrideredirect(True)
    splash_root.geometry("600x400+400+200")
    canvas = tk.Canvas(splash_root, width=600, height=400, highlightthickness=0)
    canvas.pack()

    try:
        gif = Image.open("splash.gif")
        frames = [ImageTk.PhotoImage(frame.copy().resize((600, 400))) for frame in ImageSequence.Iterator(gif)]
        def update_frame(i):
            canvas.create_image(0, 0, anchor=tk.NW, image=frames[i])
            splash_root.after(100, update_frame, (i + 1) % len(frames))
        update_frame(0)
        splash_root.after(3000, lambda: [splash_root.destroy(), root.deiconify()])
        splash_root.mainloop()
    except FileNotFoundError:
        splash_root.destroy()
        root.deiconify()
        messagebox.showwarning("Splash Missing", "splash.gif not found. Skipping splash screen.")

# ------------------------ Main GUI Setup ------------------------ #
root.title("\U0001F30D Real-Time Language Translator \U0001F30D")
root.geometry("700x550")
root.configure(bg="#F4F4F9")

# ------------------------ Background Color Animation ------------------------ #
colors = ["#1ABC9C", "#3498DB", "#9B59B6", "#E74C3C", "#F39C12", "#2C3E50"]

def change_bg_color():
    global bg_color_job
    root.configure(bg=random.choice(colors))
    bg_color_job = root.after(2000, change_bg_color)

# ------------------------ Supported Languages ------------------------ #
LANGUAGES = GoogleTranslator().get_supported_languages()

# ------------------------ Translation Function ------------------------ #
def translate_text():
    try:
        source_lang = source_lang_combo.get()
        target_lang = target_lang_combo.get()
        text = source_text.get("1.0", tk.END).strip()
        if not text:
            custom_warning("\u26A0 Please enter text to translate.")
            return
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        target_text.delete("1.0", tk.END)
        target_text.insert(tk.END, translated)
        custom_warning("")
    except Exception as e:
        custom_warning(f"\u274C Error: {str(e)}")

# ------------------------ Display Warning Messages ------------------------ #
def custom_warning(message):
    warning_label.config(text=message, fg="red")

# ------------------------ Speech Recognition ------------------------ #
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            custom_warning("\U0001F399\uFE0F Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            recognized_text = recognizer.recognize_google(audio)
            if recognized_text:
                source_text.delete("1.0", tk.END)
                source_text.insert(tk.END, recognized_text)
                custom_warning("")  
            else:
                custom_warning("\u26A0 No voice input detected.")
        except sr.UnknownValueError:
            custom_warning("\u26A0 Could not understand audio.")
        except sr.RequestError as e:
            custom_warning(f"\u274C Error connecting to service: {e}")
        except Exception as e:
            custom_warning(f"\u274C Error: {e}")

# Run speech recognition on a separate thread

def recognize_speech_thread():
    threading.Thread(target=recognize_speech, daemon=True).start()

# ------------------------ Exit Application Safely ------------------------ #
def exit_app():
    if bg_color_job:
        root.after_cancel(bg_color_job)
    if footer_style_job:
        root.after_cancel(footer_style_job)
    root.destroy()

# ------------------------ Admin Login ------------------------ #
def open_admin_login():
    login_win = tk.Toplevel(root)
    login_win.title("Admin Login")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Admin Username").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def verify_login():
        user = username_entry.get()
        passwd = password_entry.get()

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (user, passwd))
            result = cursor.fetchone()
            if result:
                show_admin_table()
                login_win.destroy()
            else:
                messagebox.showerror("Error", "Invalid Credentials")
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    tk.Button(login_win, text="Login", command=verify_login).pack(pady=10)

# ------------------------ Admin Dashboard ------------------------ #
def show_admin_table():
    admin_win = tk.Toplevel(root)
    admin_win.title("User Login Info")
    admin_win.geometry("500x300")

    tree = ttk.Treeview(admin_win, columns=("User", "Time"), show="headings")
    tree.heading("User", text="User Name")
    tree.heading("Time", text="Login Time")
    tree.pack(fill="both", expand=True)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT username, login_time FROM login_info ORDER BY login_time DESC")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------------ Main UI Components ------------------------ #
main_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief="ridge", borderwidth=2)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

welcome_label = tk.Label(main_frame, text=f"Welcome, {user_name}! \U0001F60A", font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white", pady=10)
welcome_label.pack(fill="x", pady=5)

admin_icon = tk.Button(main_frame, text="\U0001F46E Admin", font=("Arial", 10, "bold"), bg="#2C3E50", fg="white", command=open_admin_login)
admin_icon.pack(anchor="ne")

title_label = tk.Label(main_frame, text="\U0001F30D Real-Time Language Translator \U0001F30D", font=("Arial", 18, "bold"), bg="#1ABC9C", fg="white", pady=10, padx=10)
title_label.pack(fill="x", pady=(0, 10))

# Text input area
input_frame = tk.Frame(main_frame, bg="#F4F4F9")
input_frame.pack(fill="x", pady=5)

tk.Label(input_frame, text="Enter Text:", font=("Arial", 12, "bold"), bg="#F4F4F9", fg="#333333").pack(anchor="w")
source_text = tk.Text(input_frame, height=5, width=65, font=("Arial", 12), bg="#ECF0F1", borderwidth=1, relief="solid", padx=5, pady=5)
source_text.pack(padx=5, pady=5)

# Language selection
language_frame = tk.Frame(main_frame, bg="#F4F4F9")
language_frame.pack(fill="x", pady=5)

tk.Label(language_frame, text="From:", font=("Arial", 12), bg="#F4F4F9", fg="#333333").grid(row=0, column=0, padx=5, pady=5)
source_lang_combo = ttk.Combobox(language_frame, values=LANGUAGES, state="readonly", font=("Arial", 11))
source_lang_combo.grid(row=0, column=1, padx=5, pady=5)
source_lang_combo.set("english") 

tk.Label(language_frame, text="To:", font=("Arial", 12), bg="#F4F4F9", fg="#333333").grid(row=0, column=2, padx=5, pady=5)
target_lang_combo = ttk.Combobox(language_frame, values=LANGUAGES, state="readonly", font=("Arial", 11))
target_lang_combo.grid(row=0, column=3, padx=5, pady=5)
target_lang_combo.set("hindi")

# Buttons for Translate and Speak
button_frame = tk.Frame(main_frame, bg="#F4F4F9")
button_frame.pack(fill="x", pady=10)

translate_button = tk.Button(button_frame, text="\U0001F504 Translate", font=("Arial", 14, "bold"), bg="#E74C3C", fg="white", padx=10, pady=5, width=12, borderwidth=0, relief="raised", command=translate_text)
translate_button.pack(side="left", padx=20, pady=5)

speak_button = tk.Button(button_frame, text="\U0001F399\uFE0F Speak", font=("Arial", 14, "bold"), bg="#3498DB", fg="white", padx=10, pady=5, width=12, borderwidth=0, relief="raised", command=recognize_speech_thread)
speak_button.pack(side="right", padx=20, pady=5)

# Output display
tk.Label(main_frame, text="Translated Text:", font=("Arial", 12, "bold"), bg="#F4F4F9", fg="#333333").pack(anchor="w", pady=(10, 0))
target_text = tk.Text(main_frame, height=5, width=65, font=("Arial", 12), bg="#ECF0F1", borderwidth=1, relief="solid", padx=5, pady=5)
target_text.pack(padx=5, pady=5)

# Warning or status messages
tk.Label(main_frame, text="", font=("Arial", 11), fg="red", bg="#FFFFFF")
warning_label = tk.Label(main_frame, text="", font=("Arial", 11), fg="red", bg="#FFFFFF")
warning_label.pack(pady=(5, 0))

# Exit button
exit_button = tk.Button(main_frame, text="\u274C Exit", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white", padx=10, pady=5, width=12, borderwidth=0, relief="raised", command=exit_app)
exit_button.pack(pady=10)

# ------------------------ Dynamic Footer Styling ------------------------ #
def change_footer_style():
    global footer_style_job
    colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C", "#D35400"]
    styles = ["bold", "italic", "underline", "bold italic", "italic underline"]
    color = random.choice(colors)
    font_style = random.choice(styles)
    footer_label.config(fg=color, font=("Arial", 10, font_style))
    footer_style_job = root.after(2000, change_footer_style)

# Footer text
footer_label = tk.Label(
    root, 
    text="This project was driven by:\n1. Ansuman Mahapatra\n2. Biswajeet Patra\n3. Tapan Kumar Sahoo",
    font=("Arial", 10, "italic"),
    bg="#F4F4F9",
    fg="#555555",
    justify="right"
)
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

# ------------------------ Start Dynamic Events ------------------------ #
change_footer_style()
change_bg_color()
show_splash()
root.mainloop()
