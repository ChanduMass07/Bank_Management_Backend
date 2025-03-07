from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Admin@123',
    database='loggin'
)
cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('log.html')

@app.route('/log', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    
    if user:
        session['username'] = username
        return redirect('/dashboard')
    else:
        return "Login Failed. Invalid Credentials."

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
