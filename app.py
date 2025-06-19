from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Generate and store a secure encryption key (only once in real scenarios)
# Use: key = Fernet.generate_key()
# Store securely and load it here:
key = 'your-secret-key-here'  # Replace with your secure key
cipher = Fernet(key)

# =======================
# 🔹 3. Admin Credentials (✅ INSERT HERE)
# =======================
ADMIN_USERNAME = "your-admin-username"
ADMIN_PASSWORD = "your-admin-password"

# =======================
# 🔹 4. Capability Code
# =======================
VALID_CAPABILITY_CODE = "your-capability-code"
# Patterns to detect common SQL injection attempts
SQLI_PATTERNS = [
    r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
    r"(\b(OR|AND)\b\s+\w+\s*=\s*\w+)",
    r"(\bSELECT\b|\bUNION\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b)",
    r"(\bDROP\b|\bTABLE\b|\bDATABASE\b|\bFROM\b|\bWHERE\b)"
]

def is_sql_injection(text):
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    code = request.form['code']

    # Check capability code
    if code != VALID_CAPABILITY_CODE:
        return render_template("index.html", status="unauthorized")

    # Check for SQL injection in username or password
    if is_sql_injection(username) or is_sql_injection(password):
        return render_template("index.html", status="sqli")

    # Encrypt credentials using AES-256 (Fernet)
    encrypted_username = cipher.encrypt(username.encode()).decode()
    encrypted_password = cipher.encrypt(password.encode()).decode()

    print("Encrypted Username:", encrypted_username)
    print("Encrypted Password:", encrypted_password)

    # ✅ Here you could store securely in Firebase or another DB

    return render_template("index.html", status="success")

# Admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid admin credentials")
    return render_template('admin_login.html')

# Admin dashboard page
@app.route('/admin-dashboard')
def admin_dashboard():
    # For demo, no database, so show dummy data or a message
    users = [
        {"email": "user1@example.com", "code": "secure123"},
        {"email": "user2@example.com", "code": "secure123"},
    ]
    logs = [
        {"user": "user1", "input": "' OR 1=1 --", "timestamp": "2025-06-04 10:00"},
        {"user": "user2", "input": "DROP TABLE users;", "timestamp": "2025-06-04 11:00"},
    ]
    return render_template('admin_dashboard.html', users=users, logs=logs)

if __name__ == '__main__':
    app.run(debug=True)