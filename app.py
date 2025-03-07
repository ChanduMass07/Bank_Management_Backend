from flask import Flask, request, jsonify, session
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

@app.route('/api/register', methods=['POST'])
def register():
    data=request.json
    username=data['username']
    password=data['password']
    cursor.execute("INSERT INTO users (username,password) VALUES (%s,%s)",(username,password))
    db.commit()
    return jsonify({"mesage": "User registration successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data=request.json
    username=data['username']
    password=data['password']
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username,password))
    user=cursor.fetchone()
    if user:
        session['user']=username
        return jsonify({"message": "Login successful", "username":username}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__=='__main__':
    app.run(debug=True)


