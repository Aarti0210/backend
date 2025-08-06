import os
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# --- MySQL Connection (Render + PlanetScale using Environment Variables) ---
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
    port=int(os.environ.get("DB_PORT", 3306))
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return "Flask API with PlanetScale on Render is running!"

# ---------------- SIGN UP ----------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['username']      # match DB column
    email = data['email']
    password = data['password']

    # Hash password
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert user
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        db.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

# ---------------- LOGIN ----------------
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

if __name__ == "__main__":
    # Render requires host=0.0.0.0
    app.run(host="0.0.0.0", port=10000)
