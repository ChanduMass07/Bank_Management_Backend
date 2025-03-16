from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = ' '

print('Current Working Directory:', os.getcwd())
print('Templates Path:', app.template_folder)


app.config['UPLOAD_FOLDER'] = 'static/uploads'



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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        father_name = request.form['father_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        otp_verified = request.form.get('otp_verified')  # Expect 'true' if verified
        profile_picture = request.files['profile_picture']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect('/register')

        if otp_verified != "true":
            flash("Phone number not verified!", "danger")
            return redirect('/register')

        if profile_picture and allowed_file(profile_picture.filename):
            filename_ext = profile_picture.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{email}_{int(datetime.datetime.now().timestamp())}.{filename_ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            profile_picture.save(filepath)

            cursor.execute("""
                INSERT INTO users (first_name, last_name, father_name, email, phone, password, profile_picture, otp_verified)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, father_name, email, phone, password, new_filename, True))
            db.commit()

            flash("Registration successful!", "success")
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
