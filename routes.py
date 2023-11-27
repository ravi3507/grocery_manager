from app import app
from model import *
from flask import Flask, render_template, request, redirect, url_for, session

@app.route('/') 
def home_page():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user.password == password:
            if username == 'customer@gmail.com':
                return redirect(url_for('customer_dashboard',username=username))
        else:
            return redirect(url_for('customer_login'))
    return render_template('customer_login.html')

@app.route('/manager', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user.password == password:
            if username == 'manager@gmail.com':
                return redirect(url_for('manager_dashboard'))
        else:
            return redirect(url_for('manager_login'))

    return render_template('manager_login.html')


@app.route('/manager/create_category', methods=['POST'])
def create_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        add_category_to_database(category_name)
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/edit_category/<int:category_id>', methods=['POST'])
def edit_category(category_id):
    if request.method == 'POST':
        new_category_name = request.form['new_category_name']
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (new_category_name, category_id))
        conn.commit()
        conn.close()
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/remove_category/<int:category_id>', methods=['POST'])
def remove_category(category_id):
    if request.method == 'POST':
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/create_product', methods=['POST'])
def create_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = float(request.form['product_price'])
        product_quantity = int(request.form['product_quantity'])
        category_id = int(request.form['category_id'])
        product_unit=request.form['product_unit']
        add_product_to_database(product_name, product_price, product_quantity, category_id, product_unit)
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    if request.method == 'POST':
        new_product_price = float(request.form['new_product_price'])
        new_product_quantity = int(request.form['new_product_quantity'])
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET price = ?, quantity = ? WHERE id = ?', (new_product_price, new_product_quantity, product_id))
        conn.commit()
        conn.close()
        
    return redirect(url_for('manager_dashboard'))


@app.route('/manager/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    if request.method == 'POST':
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/dashboard')
def manager_dashboard():
    categories = get_all_categories_from_database()
    products = get_all_products_from_database()
    return render_template('manager_dashboard.html', categories=categories, products=products)


@app.route('/customer/dashboard/<username>', methods=['GET', 'POST'])
def customer_dashboard(username):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    available_categories = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE name LIKE ?", ('%' + search_query + '%',))
        section_search_results = cursor.fetchall()
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_query + '%',))
        product_search_results = cursor.fetchall()
        search_results = []
        for section in section_search_results:
            search_results.append({
                'Type': 'Category',
                'Name': section[1],
                'ID': section[0]
            })
        for product in product_search_results:
            search_results.append({
                'Type': 'Product',
                'Name': product[1],
                'Price': product[2],
                'Quantity': product[3],
                'Unit': product[4],
                'ID': product[0]
            })
        conn.close()
        return render_template('customer_dashboard.html', username=username, search_results=search_results)
    return render_template('customer_dashboard.html', username=username, available_categories=available_categories)

@app.route('/customer/cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}  
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    
    if product[3]<quantity:
        return f'only {product[3]} left' 
    
    elif product[3]<0:
        return f'out of stock'
        
    else:
        cart_item = {
            'name': product[1],
            'price': product[2],
            'quantity': quantity,
            'subtotal': product[2] * quantity,
            'unit' : product[5]
        }

        if product_id in session['cart']:
            session['cart'][product_id]['quantity'] += quantity
            session['cart'][product_id]['subtotal'] += cart_item['subtotal']
        else:
            session['cart'][product_id] = cart_item

        cursor.execute('SELECT * FROM cart WHERE product_id = ?', (product_id,))
        cartitem = cursor.fetchone()

        if cartitem is None:
            cursor.execute('INSERT INTO cart (product_id, product_name, price, quantity, subtotal, unit) VALUES (?, ?, ?, ?, ?, ?)',
                        (product_id, cart_item['name'], cart_item['price'], quantity, cart_item['subtotal'], cart_item['unit']))

        else:
            updated_quantity = cartitem[3] + quantity
            updated_subtotal = cartitem[4] + cart_item['subtotal']
            cursor.execute('UPDATE cart SET quantity = ?, subtotal = ? WHERE product_id = ?', (updated_quantity, updated_subtotal, product_id))
        conn.commit()
        conn.close()
        return redirect(request.referrer)

@app.route('/customer/cart', methods=['GET'])
def view_cart():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()
    total_price = sum(item[4] for item in cart_items)
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/customer/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/customer/display_category_products/<int:category_id>', methods=['GET'])
def display_category_products(category_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE category_id=?", (category_id,))
    products = cursor.fetchall()
    conn.close()
    category_name = get_category_name(category_id)

    return render_template('category.html', products=products, category_name=category_name)



@app.route('/customer/checkout', methods=['POST'])
def checkout():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()
    for item in cart_items:
        cursor.execute('SELECT quantity FROM products WHERE id = ?', (item[0],))
        product_quantity = cursor.fetchone()[0]
        updated_quantity = product_quantity - item[3]
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (updated_quantity, item[0],))
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()
    session.pop('cart', None)
    return redirect(url_for('customer_dashboard', username='username'))