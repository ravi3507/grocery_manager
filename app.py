from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()



cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        unit TEXT NOT NULL,       
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        product_id INTEGER,
        product_name TEXT,
        price REAL,
        quantity INTEGER,
        subtotal REAL,
        unit TEXT
    )
''')

conn.commit()
conn.close()

from model import *
from routes import *


if __name__ == '__main__':
    app.run(debug=True)