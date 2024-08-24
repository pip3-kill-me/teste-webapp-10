from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# In-memory storage for messages
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            messages.append(message)
        return redirect(url_for('index'))
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
