from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
import os
import json
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app)
online_users = 0

# File where messages will be stored
MESSAGE_FILE = 'data/messages.json'
UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# Function to compress and resize image
def compress_and_resize_image(image_path, max_size=(512, 512), quality=10):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img.save(image_path, quality=quality, optimize=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_text = request.form['message']
        username = request.form['username']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        image_file = request.files.get('image')
        
        image_path = None
        if image_file:
            image_filename = 'evidencia_' +datetime.now().strftime("%Y%m%d%H%M%S") + '_' + image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            compress_and_resize_image(image_path)
            image_path = url_for('static', filename=f'uploads/{image_filename}')

        
        message_data = {'text': message_text, 'timestamp': timestamp, 'username': username}
        
        if image_path:
            message_data['image'] = image_path

        messages.append(message_data)
        save_messages(messages)
        socketio.emit('message_update', message_data)

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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
