import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import random
import speech_recognition as sr
import threading

root = tk.Tk()
root.title("🌍 Real-Time Language Translator 🌍")
root.geometry("700x500")
root.configure(bg="#F4F4F9")
colors = ["#1ABC9C", "#3498DB", "#9B59B6", "#E74C3C", "#F39C12", "#2C3E50"]

def change_bg_color():
    root.configure(bg=random.choice(colors))
    root.after(2000, change_bg_color)
LANGUAGES = GoogleTranslator().get_supported_languages()

def translate_text():
    try:
        source_lang = source_lang_combo.get()
        target_lang = target_lang_combo.get()
        text = source_text.get("1.0", tk.END).strip()
        if not text:
            custom_warning("⚠ Please enter text to translate.")
            return
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        target_text.delete("1.0", tk.END)
        target_text.insert(tk.END, translated)
        custom_warning("")
    except Exception as e:
        custom_warning(f"❌ Error: {str(e)}")
        
def custom_warning(message):
    warning_label.config(text=message, fg="red")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            custom_warning("🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            recognized_text = recognizer.recognize_google(audio)
            if recognized_text:
                source_text.delete("1.0", tk.END)
                source_text.insert(tk.END, recognized_text)
                custom_warning("")  
            else:
                custom_warning("⚠ No voice input detected.")
        except sr.UnknownValueError:
            custom_warning("⚠ Could not understand audio.")
        except sr.RequestError as e:
            custom_warning(f"❌ Error connecting to service: {e}")
        except Exception as e:
            custom_warning(f"❌ Error: {e}")
            
def recognize_speech_thread():
    threading.Thread(target=recognize_speech, daemon=True).start()
    
main_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief="ridge", borderwidth=2)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
title_label = tk.Label(main_frame, text="🌍 Real-Time Language Translator 🌍", font=("Arial", 18, "bold"), bg="#1ABC9C", fg="white", pady=10, padx=10)
title_label.pack(fill="x", pady=(0, 10))
input_frame = tk.Frame(main_frame, bg="#F4F4F9")
input_frame.pack(fill="x", pady=5)
tk.Label(input_frame, text="Enter Text:", font=("Arial", 12, "bold"), bg="#F4F4F9", fg="#333333").pack(anchor="w")
source_text = tk.Text(input_frame, height=5, width=65, font=("Arial", 12), bg="#ECF0F1", borderwidth=1, relief="solid", padx=5, pady=5)
source_text.pack(padx=5, pady=5)
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
button_frame = tk.Frame(main_frame, bg="#F4F4F9")
button_frame.pack(fill="x", pady=10)
translate_button = tk.Button(button_frame, text="🔄 Translate", font=("Arial", 14, "bold"), bg="#E74C3C", fg="white", padx=10, pady=5, width=12,borderwidth=0, relief="raised", command=translate_text)
translate_button.grid(row=0, column=0, padx=10)
speak_button = tk.Button(button_frame, text="🎙️ Speak", font=("Arial", 14, "bold"), bg="#3498DB", fg="white", padx=10, pady=5, width=12,borderwidth=0, relief="raised", command=recognize_speech_thread)
speak_button.grid(row=0, column=1, padx=10)
tk.Label(main_frame, text="Translated Text:", font=("Arial", 12, "bold"), bg="#F4F4F9", fg="#333333").pack(anchor="w", pady=(10, 0))
target_text = tk.Text(main_frame, height=5, width=65, font=("Arial", 12), bg="#ECF0F1", borderwidth=1, relief="solid", padx=5, pady=5)
target_text.pack(padx=5, pady=5)
warning_label = tk.Label(main_frame, text="", font=("Arial", 11), fg="red", bg="#FFFFFF")
warning_label.pack(pady=(5, 0))
footer_label = tk.Label(root, text="This project was made by:\n1. Ansuman Mahapatra\n2. Biswajeet Patra\n3. Tapan Kumar Sahoo", font=("Arial", 10, "italic"), bg="#F4F4F9", fg="#555555", justify="center")
footer_label.pack(side="bottom", pady=5)
change_bg_color()
root.mainloop()