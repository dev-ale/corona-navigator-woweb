# app.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__, static_folder='dist/',    static_url_path='/')


# Set up the index route
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
