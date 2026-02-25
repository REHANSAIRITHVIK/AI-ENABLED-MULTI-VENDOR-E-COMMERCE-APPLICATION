import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'rehan_multi_vendor_tech_2026'

# --- DATABASE CONFIGURATION ---
DB_PATH = os.path.join('instance', 'ecommerce.db')
if not os.path.exists('instance'):
    os.makedirs('instance')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Users: admin, vendor, customer
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL)''')
    # Products: Includes image_path for your subfolders
    conn.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        image_path TEXT NOT NULL,
        vendor_id INTEGER,
        FOREIGN KEY (vendor_id) REFERENCES users (id))''')
    # Orders: Tracks customer purchases
    conn.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        product_name TEXT,
        image_path TEXT,
        total REAL,
        status TEXT,
        date TEXT,
        FOREIGN KEY (customer_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

init_db()

# --- THE 12 CATEGORIES ---
CATEGORIES = [
    'laptops', 'mobiles', 'headphones', 'ac', 'tv', 
    'refrigerator', 'coolers', 'books', 'shoes', 
    'watches', 'mens_fashion', 'womens_fashions'
]

# --- AUTHENTICATION ROUTES ---

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Redirect logic based on role to prevent BuildErrors
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif session['role'] == 'vendor':
        return redirect(url_for('vendor_dashboard'))
    else:
        return redirect(url_for('customer_dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session.update({'user_id': user['id'], 'username': user['username'], 'role': user['role']})
            return redirect(url_for('home'))
        flash('Invalid Username or Password!')
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            return redirect(url_for('login'))
        except:
            flash('Username already exists!')
        finally:
            conn.close()
    return render_template('auth/register.html')

# --- VENDOR ROUTES (Corrected for BuildError) ---

@app.route('/vendor/dashboard')
def vendor_dashboard():
    conn = get_db_connection()
    prods = conn.execute('SELECT * FROM products WHERE vendor_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    # Note: Variable name 'products' matches HTML loops to prevent UndefinedError
    return render_template('vendor/dashboard.html', products=prods)

@app.route('/vendor/products')
def vendor_view_products():
    # This route specifically handles the sidebar/dashboard links
    conn = get_db_connection()
    prods = conn.execute('SELECT * FROM products WHERE vendor_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('vendor/dashboard.html', products=prods)

@app.route('/vendor/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, category, price, image_path, vendor_id) VALUES (?, ?, ?, ?, ?)',
                     (request.form['name'], request.form['category'], request.form['price'], request.form['image_path'], session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('vendor_dashboard'))
    return render_template('vendor/add_product.html', categories=CATEGORIES)

@app.route('/vendor/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ? AND vendor_id = ?', (product_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('vendor_dashboard'))



# --- CUSTOMER ROUTES ---

@app.route('/customer/dashboard')
def customer_dashboard():
    conn = get_db_connection()
    prods = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('customer/dashboard.html', products=prods, categories=CATEGORIES)

@app.route('/products/<category>')
def view_products(category):
    conn = get_db_connection()
    prods = conn.execute('SELECT * FROM products WHERE category = ?', (category,)).fetchall()
    conn.close()
    return render_template('customer/view_products.html', products=prods, category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return render_template('customer/product.html', product=product)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('customer_dashboard'))

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    conn = get_db_connection()
    cart_items = []
    total = 0
    for pid in cart_ids:
        item = conn.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
        if item:
            cart_items.append(item)
            total += item['price']
    conn.close()
    return render_template('customer/cart.html', cart_items=cart_items, total_price=total)

@app.route('/checkout')
def checkout():
    # Calculate total again for the checkout page
    cart_ids = session.get('cart', [])
    conn = get_db_connection()
    total = 0
    for pid in cart_ids:
        item = conn.execute('SELECT price FROM products WHERE id = ?', (pid,)).fetchone()
        if item:
            total += item['price']
    conn.close()
    # Pass total_price so it doesn't show ₹0.00
    return render_template('customer/checkout.html', total_price=total)

@app.route('/search')
def search_products():
    query = request.args.get('query', '')
    conn = get_db_connection()
    # SQL query to search for the keyword in name or category
    results = conn.execute(
        'SELECT * FROM products WHERE name LIKE ? OR category LIKE ?',
        ('%' + query + '%', '%' + query + '%')
    ).fetchall()
    conn.close()
    return render_template('customer/search_results.html', products=results, query=query)

@app.route('/payment_status/<status>')
def payment_status(status):
    if status == 'success' and 'cart' in session:
        conn = get_db_connection()
        for pid in session['cart']:
            p = conn.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
            if p:
                conn.execute('INSERT INTO orders (customer_id, product_name, image_path, total, status, date) VALUES (?, ?, ?, ?, ?, ?)',
                             (session['user_id'], p['name'], p['image_path'], p['price'], 'Paid', datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        session.pop('cart')
    return render_template('customer/payment_status.html', status=status)

@app.route('/orders')
def orders():
    conn = get_db_connection()
    user_orders = conn.execute('SELECT * FROM orders WHERE customer_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('customer/orders.html', orders=user_orders)

@app.route('/profile')
def profile():
    return render_template('customer/profile.html')

# --- ADMIN ROUTES ---

@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    products = conn.execute('SELECT * FROM products').fetchall()
    revenue = conn.execute('SELECT SUM(total) as rev FROM orders').fetchone()
    conn.close()
    return render_template('admin/dashboard.html', users=users, products=products, total_revenue=revenue['rev'] or 0)

@app.route('/admin/customers')
def admin_customers():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('admin/customers.html', users=users)

@app.route('/admin/products')
def admin_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('admin/products.html', products=products)

@app.route('/admin/categories')
def admin_categories():
    conn = get_db_connection()
    cat_data = []
    for cat in CATEGORIES:
        count = conn.execute('SELECT COUNT(*) FROM products WHERE category = ?', (cat,)).fetchone()[0]
        cat_data.append({'name': cat, 'count': count})
    conn.close()
    return render_template('admin/categories.html', categories=cat_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)