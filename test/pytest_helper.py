import sys
import os
import pytest

ROOT_DIR = os.path.dirname(os.path.abspath('app.py'))  # TODO, find better solution
sys.path.append(ROOT_DIR)
import app

from flask_pymongo import PyMongo


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    app.mongo = init_db()
    reset_db(app.mongo)
    seed_db(app.mongo)
    yield app.app.test_client()
    reset_db(app.mongo)


@pytest.fixture
def database():
    return init_db()


def init_db():
    app.app.config['MONGO_URI'] = 'mongodb://localhost:27017/testDB'
    return PyMongo(app.app)


def seed_db(db):
    db.db.incidences.insert_many([
        {'canton': 'ZH', 'date': '2021-05-12', 'incident': 100.90817356205852, 'name': 'Aeugst am Albis'},
        {'canton': 'BL', 'date': '2021-05-12', 'incident': 241.0, 'name': 'Oberwil'}
    ])


def reset_db(db):
    query = {"incident": {"$gt": -1}}
    db.db.incidences.delete_many(query)
