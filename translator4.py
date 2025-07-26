import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import random
import speech_recognition as sr

# Initialize window
root = tk.Tk()
root.title("🌍 Real-Time Language Translator 🌍")
root.geometry("600x500")

colors = ["#1ABC9C", "#3498DB", "#9B59B6", "#E74C3C", "#F39C12", "#2C3E50"]

def change_bg_color():
    """Change background color every 2 seconds."""
    root.configure(bg=random.choice(colors))
    root.after(2000, change_bg_color)

# Get supported languages
LANGUAGES = GoogleTranslator().get_supported_languages()

def translate_text():
    try:
        source_lang = source_lang_combo.get()
        target_lang = target_lang_combo.get()
        text = source_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("⚠ Warning", "Please enter text to translate.")
            return

        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        target_text.delete("1.0", tk.END)
        target_text.insert(tk.END, translated)
    except Exception as e:
        messagebox.showerror("❌ Error", str(e))

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("🎙️ Speak Now", "Listening...")
            audio = recognizer.listen(source)
            recognized_text = recognizer.recognize_google(audio)
            source_text.delete("1.0", tk.END)
            source_text.insert(tk.END, recognized_text)
        except sr.UnknownValueError:
            messagebox.showwarning("⚠ Warning", "Could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("❌ Error", f"Could not request results; {e}")

# UI Elements
title_label = tk.Label(root, text="🌍 Real-Time Language Translator 🌍", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white", pady=10)
title_label.pack(fill="x")

# Input Text
tk.Label(root, text="Enter Text:", font=("Arial", 12, "bold"), bg=root.cget("bg"), fg="blue").pack(anchor="w", padx=10, pady=5)
source_text = tk.Text(root, height=5, width=50, font=("Arial", 12))
source_text.pack(padx=10, pady=5)

# Language Selection
frame = tk.Frame(root, bg=root.cget("bg"))
frame.pack(pady=5)

tk.Label(frame, text="From:", font=("Arial", 12), bg=root.cget("bg"), fg="black").grid(row=0, column=0, padx=10, pady=5)
source_lang_combo = ttk.Combobox(frame, values=LANGUAGES, state="readonly", font=("Arial", 11))
source_lang_combo.grid(row=0, column=1, padx=10, pady=5)
source_lang_combo.set("english") 

tk.Label(frame, text="To:", font=("Arial", 12), bg=root.cget("bg"), fg="black").grid(row=0, column=2, padx=10, pady=5)
target_lang_combo = ttk.Combobox(frame, values=LANGUAGES, state="readonly", font=("Arial", 11))
target_lang_combo.grid(row=0, column=3, padx=10, pady=5)
target_lang_combo.set("hindi") 

# Buttons (Translate + Speak)
button_frame = tk.Frame(root, bg=root.cget("bg"))
button_frame.pack(pady=10)

translate_button = tk.Button(button_frame, text="🔄 Translate", font=("Arial", 14, "bold"), bg="#E74C3C", fg="white", padx=10, pady=5, command=translate_text)
translate_button.grid(row=0, column=0, padx=5)

speak_button = tk.Button(button_frame, text="🎙️ Speak", font=("Arial", 14, "bold"), bg="#3498DB", fg="white", padx=10, pady=5,command=recognize_speech)
speak_button.grid(row=0, column=1, padx=5)

# Translated Text
tk.Label(root, text="Translated Text:", font=("Arial", 12, "bold"), bg=root.cget("bg"), fg="blue").pack(anchor="w", padx=10, pady=5)
target_text = tk.Text(root, height=5, width=50, font=("Arial", 12), bg="#ECF0F1")
target_text.pack(padx=10, pady=5)

# Footer
footer_label = tk.Label(root, text="This project was made by:\n1. Ansuman Mahapatra\n2. Biswajeet Patra\n3. Tapan Kumar Sahoo", font=("Arial", 10, "italic"), bg=root.cget("bg"), fg="black", justify="right")
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

# Start background color change
change_bg_color()

# Run the app
root.mainloop()
