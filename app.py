from flask import Flask, request, jsonify
import random
import string
import sqlite3

app = Flask(_name_)

# Function to generate a unique ID
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Database connection
conn = sqlite3.connect('relationships.db')
c = conn.cursor()

# Create Users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Password TEXT NOT NULL,
                UniqueID TEXT UNIQUE
            )''')

# Create Relationships table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS Relationships (
                RelationshipID INTEGER PRIMARY KEY AUTOINCREMENT,
                Partner1ID INTEGER,
                Partner2ID INTEGER,
                StartDate DATE,
                Milestones TEXT,
                FOREIGN KEY (Partner1ID) REFERENCES Users(UserID),
                FOREIGN KEY (Partner2ID) REFERENCES Users(UserID)
            )''')

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    unique_id = generate_unique_id()

    try:
        c.execute("INSERT INTO Users (Username, Password, UniqueID) VALUES (?, ?, ?)", (username, password, unique_id))
        conn.commit()
        return jsonify({'message': 'User registered successfully', 'unique_id': unique_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

# Route to link partner IDs
@app.route('/link', methods=['POST'])
def link_partner():
    data = request.get_json()
    user_id = data['user_id']
    partner_id = data['partner_id']

    try:
        c.execute("INSERT INTO Relationships (Partner1ID, Partner2ID) VALUES (?, ?)", (user_id, partner_id))
        conn.commit()
        return jsonify({'message': 'Partner linked successfully'}), 200
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Relationship already exists'}), 400

# Route to get relationship information
@app.route('/relationship/<unique_id>', methods=['GET'])
def get_relationship(unique_id):
    c.execute('''SELECT * FROM Users WHERE UniqueID=?''', (unique_id,))
    user = c.fetchone()

    if user:
        user_id = user[0]
        c.execute('''SELECT * FROM Relationships WHERE Partner1ID=? OR Partner2ID=?''', (user_id, user_id))
        relationships = c.fetchall()
        return jsonify({'relationships': relationships}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if _name_ == '_main_':
    app.run(debug=True)
