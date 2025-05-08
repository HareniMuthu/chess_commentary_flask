from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import subprocess
import os

app = Flask(__name__)
app.secret_key = "ThisIsNotASecret:p"

# SQLite Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Home page
@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')  # Authenticated user sees home
    else:
        return render_template('index.html', message="Hello!")  # Public landing

# Registration
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('register.html', message="Username already exists. Try another.")
    return render_template('register.html', message="Welcome to the Chess Commentary App!")

# Login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session['logged_in'] = True
            return redirect(url_for('index'))  # Redirect to home after login
        return render_template('login.html', message="Incorrect username or password.")

# Logout
@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

# Launch the Chess Game and show success message
@app.route('/launch')
def launch():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Path to the compiled .exe file (update path if needed)
    exe_path = 'dist/chess_commentator.exe'
    subprocess.Popen([exe_path])  # Launch the .exe in background

    return render_template('ready.html')  # Display success message page

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database is created
    app.run(debug=True)
