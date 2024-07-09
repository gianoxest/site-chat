from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, emit
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

users = {}  # Format: {username: {'password': password, 'color': color}}
messages = []

def generate_color():
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFF5']
    return random.choice(colors)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username already exists! Please choose a different username.'
        users[username] = {'password': password, 'color': generate_color()}
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        return 'Invalid username or password! Please try again.'
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', username=session['username'])

@socketio.on('connect')
def connect():
    if 'username' in session:
        emit('message', {'username': 'System', 'message': f'{session["username"]} joined the chat!'})
    else:
        return False

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    color = users.get(username, {}).get('color', '#000000')
    message = {'username': username, 'message': data['message'], 'color': color}
    messages.append(message)
    emit('message', message, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    if 'username' in session:
        emit('message', {'username': 'System', 'message': f'{session["username"]} left the chat!'})
        users.pop(session['username'], None)

if __name__ == '__main__':
    socketio.run(app, debug=True)
