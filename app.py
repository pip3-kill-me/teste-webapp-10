from flask import Flask, request, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_text = request.form['message']
        username = request.form['username']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages.append({'text': message_text, 'timestamp': timestamp, 'username' : username})
        save_messages(messages)  # Save messages after each new message
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
