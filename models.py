
import sqlite3
import hashlib

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        nickname TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        product TEXT,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def create_user(email, password, nickname):
    conn = get_db()
    c = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (email, password, nickname) VALUES (?, ?, ?)", (email, hashed, nickname))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "email": row[1], "password": row[2], "nickname": row[3]}
    return None

def check_password(stored_hash, password):
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

def create_order(email, product, status):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO orders (email, product, status) VALUES (?, ?, ?)", (email, product, status))
    conn.commit()
    conn.close()

def get_orders_by_user(email):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE email = ?", (email,))
    rows = c.fetchall()
    conn.close()
    return rows
