from flask import Flask, render_template, request, redirect, url_for
from database import connect_db

app = Flask(_name_)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect(url_for('relationship'))
    return render_template('login.html')

@app.route('/relationship')
def relationship():
    # Fetch relationship information from the database and pass it to the template
    return render_template('relationship.html')

if _name_ == '_main_':
    app.run(debug=True)
