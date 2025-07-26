import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

root = tk.Tk()
root.title("Real-Time Language Translator")
root.geometry("600x400")
root.configure(bg="#f4f4f4")

LANGUAGES = GoogleTranslator().get_supported_languages()

def translate_text():
    try:
        source_lang = source_lang_combo.get()
        target_lang = target_lang_combo.get()
        text = source_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text to translate.")
            return

        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        target_text.delete("1.0", tk.END)
        target_text.insert(tk.END, translated)
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Label(root, text="Enter Text:", font=("Arial", 12, "bold"), bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=10, sticky="w")
source_text = tk.Text(root, height=5, width=50)
source_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

tk.Label(root, text="From Language:", font=("Arial", 12), bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5, sticky="w")
source_lang_combo = ttk.Combobox(root, values=LANGUAGES, state="readonly")
source_lang_combo.grid(row=2, column=1, padx=10, pady=5)
source_lang_combo.set("english")  

tk.Label(root, text="To Language:", font=("Arial", 12), bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5, sticky="w")
target_lang_combo = ttk.Combobox(root, values=LANGUAGES, state="readonly")
target_lang_combo.grid(row=3, column=1, padx=10, pady=5)
target_lang_combo.set("hindi")  

translate_button = tk.Button(root, text="Translate", font=("Arial", 12, "bold"), bg="#00aaff", fg="white", command=translate_text)
translate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Translated Text:", font=("Arial", 12, "bold"), bg="#f4f4f4").grid(row=5, column=0, padx=10, pady=5, sticky="w")
target_text = tk.Text(root, height=5, width=50)
target_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

footer_label = tk.Label(root, text="This project was made by:\n1. Ansuman Mahapatra\n2. Biswajeet Patra\n3. Tapan Kumar Sahoo", 
                        font=("Arial", 10, "italic"), bg=root.cget("bg"), fg="white", justify="right")
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10) 

root.mainloop()
