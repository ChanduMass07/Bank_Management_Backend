from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = ' '

print('Current Working Directory:', os.getcwd())
print('Templates Path:', app.template_folder)

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Admin@123',
    database='Bank_Management'
)
cursor = db.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    balance FLOAT DEFAULT 0.0
)
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS contact_us (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL
)
""")

db.commit()

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user'] = username
            return redirect(url_for('admin'))
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin():
    
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/balance')
def balance():
    if 'user' in session:
        cursor.execute("SELECT balance FROM users WHERE username=%s", (session['user'],))
        balance = cursor.fetchone()[0]
        return render_template('balance.html', balance=balance)
    return redirect('/login')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'user' in session:
        if request.method == 'POST':
            amount = float(request.form['amount'])
            cursor.execute("UPDATE users SET balance = balance + %s WHERE username=%s", (amount, session['user']))
            db.commit()
            return redirect('/balance')
        return render_template('deposit.html')
    return redirect('/login')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'user' in session:
        if request.method == 'POST':
            amount = float(request.form['amount'])
            cursor.execute("SELECT balance FROM users WHERE username=%s", (session['user'],))
            balance = cursor.fetchone()[0]
            if balance >= amount:
                cursor.execute("UPDATE users SET balance = balance - %s WHERE username=%s", (amount, session['user']))
                db.commit()
            return redirect('/balance')
        return render_template('withdraw.html')
    return redirect('/login')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        try:
            cursor.execute("INSERT INTO contact_us (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
            db.commit()
            flash('Your message has been submitted successfully!', 'success')
        except Exception as e:
            flash('Error submitting message. Please try again.', 'danger')
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/contact/message')
def view_messages():
    cursor.execute("SELECT * FROM contact_us")
    messages = cursor.fetchall()
    return render_template('message.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
