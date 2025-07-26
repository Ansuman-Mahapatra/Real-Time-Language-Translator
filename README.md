# 🌐 Real-Time Language Translator with Voice Input 🎙️

This is a **real-time language translator desktop application** built using **Python (Tkinter GUI)**. It supports **voice recognition**, **Google translation**, and **MySQL login tracking** with a beautiful animated splash screen. Ideal for language learners and communication across different languages!

---

## 🧠 Key Features

- 🎤 **Speech-to-text** using microphone input
- 🌍 **Text translation** between 100+ languages via Google Translate
- 💬 **Text input/output** via GUI interface
- 🧑‍💼 **Admin panel** to view user login logs
- 📦 **MySQL** used for saving login time and user info
- 🎞️ Animated **splash screen**
- 🌈 Dynamic background and footer animations

---

## 🛠️ Technologies Used

- **Python 3**
- `Tkinter` – GUI
- `deep_translator` – For translations
- `speech_recognition` – Voice input
- `mysql-connector-python` – MySQL database interaction
- `Pillow` – For animated splash screen (`splash.gif`)
- `threading` – To run tasks like voice recognition asynchronously

---

## 🗃️ Folder Structure

PyLanguageTranslator/
├── translator8.py # Main program file
├── requirements.txt # List of all required libraries
├── splash.gif # Animated splash screen (optional but recommended)
└── README.md # This file

---

## 🧪 How to Run

### 📥 1. Install Dependencies

Activate your virtual environment (if any) and run:

```bash
pip install -r requirements.txt
 ```
▶ 2. Run the App
```bash
python translator8.py
 ```

 🗃️ 3. MySQL Setup
Create a database: PythonTranslator
Run these SQL queries in MySQL Workbench:

```bash
CREATE TABLE login_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    login_time DATETIME
);

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO admin (username, password) VALUES
('admin1', 'admin@123'),
('ansuman', 'ansu@0747');
 ```

 👤 Admin Panel
Click the 👮 Admin button

Enter the credentials (e.g., admin1 / admin@123)

View login records of all users

💡 Notes
Make sure your microphone is working for voice input.

If pyaudio fails to install on Windows, use:
```bash
pip install pipwin
pipwin install pyaudio
```