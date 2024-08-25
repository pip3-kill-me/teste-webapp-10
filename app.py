from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# File where messages will be stored
MESSAGE_FILE = 'data/messages.json'

# Function to load messages from the file
def load_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as file:
            return json.load(file)
    return []

# Function to save messages to the file
def save_messages(messages):
    if not os.path.exists('data'):
        os.makedirs('data')
    with open(MESSAGE_FILE, 'w') as file:
        json.dump(messages, file)

# Load messages when the app starts
messages = load_messages()

# Track the number of online users
online_users = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', messages=messages)

@socketio.on('connect')
def handle_connect():
    global online_users
    online_users += 1
    emit('update_user_count', online_users, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global online_users
    online_users -= 1
    emit('update_user_count', online_users, broadcast=True)

@socketio.on('new_message')
def handle_new_message(data):
    message_text = data['message']
    username = data['username']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_message = {'text': message_text, 'timestamp': timestamp, 'username': username}
    messages.append(new_message)
    save_messages(messages)
    emit('message_update', new_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

