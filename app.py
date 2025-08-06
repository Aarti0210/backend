from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import mysql.connector
import os

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# MySQL connection with SSL required for PlanetScale
import mysql.connector, os

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
        ssl_ca="/etc/ssl/certs/ca-certificates.crt"
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Database connected!")
except Exception as e:
    print("❌ Database connection failed:", e)
    db = None
    cursor = None

cursor = db.cursor(dictionary=True)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['username']
    email = data['email']
    password = data['password']

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        db.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({
            "message": "Login successful!",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
