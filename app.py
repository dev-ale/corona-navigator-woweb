# app.py
from flask import Flask, request, jsonify
import os
from flask_pymongo import PyMongo
import logging.config

app = Flask(__name__, static_folder='dist/', static_url_path='/')

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('LOGGER')
errorLogger = logging.getLogger('ERROR-LOGGER')


# Set up the index route
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/incidences', methods=['GET'])
def incidences():
    try:
        logger.info('call to: /api/incidences')
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
    except Exception as ex:
        errorLogger.error(str(ex))


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
