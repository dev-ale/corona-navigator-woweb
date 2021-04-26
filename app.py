# app.py
from flask import Flask, request, jsonify
import os
from flask_pymongo import PyMongo

app = Flask(__name__, static_folder='dist/',    static_url_path='/')

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

# Set up the index route
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/incidences', methods=['GET'])
def incidences():
    ins = mongo.db.incidences.find(
        {},
        {
            '_id': 0,
            'name': 1,
            'canton': 1,
            'date': 1,
            'incident': 1
        }
    )
    return jsonify(list(ins))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
