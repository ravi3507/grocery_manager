import sqlite3
def get_all_categories_from_database():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_all_products_from_database():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def add_category_to_database(category_name):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
    conn.commit()
    conn.close()

def add_product_to_database(product_name, product_price, product_quantity, category_id, product_unit):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, quantity, category_id, unit) VALUES (?, ?, ?, ?, ?)',
                   (product_name, product_price, product_quantity, category_id, product_unit))
    conn.commit()
    conn.close()

def get_category_name(category_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
    category_name = cursor.fetchone()[0]
    conn.close()
    return category_name


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = [
    User(1, 'manager@gmail.com', 'manager@123'),
    User(2, 'customer@gmail.com', 'customer@123'),
]

def get_user(username):
    for user in users:
        if user.username == username:
            return user
    return None