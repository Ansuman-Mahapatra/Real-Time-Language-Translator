import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

root = tk.Tk()
root.title(" Real-Time Language Translator ")
root.geometry("600x450")
root.configure(bg="#2C3E50")  

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

title_label = tk.Label(root, text="🌍 Real-Time Language Translator 🌍", 
                    font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white", 
                    pady=10)
title_label.pack(fill="x")

tk.Label(root, text="Enter Text:", font=("Arial", 12, "bold"), 
        bg="#2C3E50", fg="white").pack(anchor="w", padx=10, pady=5)
source_text = tk.Text(root, height=5, width=50, font=("Arial", 12))
source_text.pack(padx=10, pady=5)

frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=5)

tk.Label(frame, text="From:", font=("Arial", 12), bg="#2C3E50", fg="white").grid(row=0, column=0, padx=10, pady=5)
source_lang_combo = ttk.Combobox(frame, values=LANGUAGES, state="readonly", font=("Arial", 11))
source_lang_combo.grid(row=0, column=1, padx=10, pady=5)
source_lang_combo.set("english")  

tk.Label(frame, text="To:", font=("Arial", 12), bg="#2C3E50", fg="white").grid(row=0, column=2, padx=10, pady=5)
target_lang_combo = ttk.Combobox(frame, values=LANGUAGES, state="readonly", font=("Arial", 11))
target_lang_combo.grid(row=0, column=3, padx=10, pady=5)
target_lang_combo.set("hindi")  

translate_button = tk.Button(root, text="🔄 Translate", font=("Arial", 14, "bold"), 
                            bg="#E74C3C", fg="white", padx=10, pady=5, 
                            command=translate_text)
translate_button.pack(pady=10)

tk.Label(root, text="Translated Text:", font=("Arial", 12, "bold"), 
        bg="#2C3E50", fg="white").pack(anchor="w", padx=10, pady=5)
target_text = tk.Text(root, height=5, width=50, font=("Arial", 12), bg="#ECF0F1")
target_text.pack(padx=10, pady=5)

footer_label = tk.Label(root, text="This project was made by:\n1. Ansuman Mahapatra\n2. Biswajeet Patra\n3. Tapan Kumar Sahoo", 
                        font=("Arial", 10, "italic"), bg=root.cget("bg"), fg="white", justify="right")
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10) 

root.mainloop()
