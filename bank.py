from flask import Flask, jsonify, request, session
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

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

db.commit()

@app.route('/')
def home():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
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
            return redirect('/')
    return send_file('')

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

if __name__ == '__main__':
    app.run(debug=True)
