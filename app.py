from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import string

app = Flask(_name_)

# Function to generate a unique relationship number
def generate_relationship_number():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('relationships.db')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        try:
            unique_id = generate_relationship_number()
            cursor.execute("INSERT INTO Users (Username, Password, UniqueID) VALUES (?, ?, ?)", (username, password, unique_id))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            error_message = "Error occurred: " + str(e)
            return render_template('register.html', error=error_message)
        finally:
            conn.close()
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username=? AND Password=?", (username, password))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('relationship', unique_id=user[3]))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Route for displaying relationship status
@app.route('/relationship/<unique_id>')
def relationship(unique_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Relationships WHERE Partner1ID=? OR Partner2ID=?", (unique_id, unique_id))
    relationships = cursor.fetchall()
    conn.close()
    return render_template('relationship.html', relationships=relationships)

if _name_ == '_main_':
    app.run(debug=True)
         
   
