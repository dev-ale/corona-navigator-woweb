from pytest_helper import *
import app
app.mongo = init_db()
from db_update import *

incidences = {
    'BLBS': [{
        'bfsNr': 2763,
        'date': '2021-05-04',
        'incidence': 318
    }],
    'ZH': [{
        'bfsNr': 1,
        'date': '2021-05-04',
        'incidence': 100.9
    }, {
        'bfsNr': 298,
        'date': '2021-05-04',
        'incidence': 92.0
    }]
}

municipalities = {
    'BLBS': [{
        'bfsNr': 2763,
        'name': 'Arlesheim',
        'canton': 'BL',
        'area': 6.9,
        'population': 9129
    }],
    'ZH': [{
        'bfsNr': 1,
        'name': 'Aeugst am Albis',
        'canton': 'ZH',
        'area': 7.9,
        'population': 1982
    }, {
        'bfsNr': 298,
        'name': 'Wiesendangen',
        'canton': 'ZH',
        'area': 19.13,
        'population': 6521
    }]
}

def test_update_db(database, mocker):
    assert database.db.incidences.count_documents({}) == 0
    mocker.patch('db_update.get_incidences_from_canton_services', return_value=incidences)
    mocker.patch('db_update.get_municipalities_from_canton_services', return_value=municipalities)
    update_db()
    incidence = database.db.incidences.find_one({'bfsNr': 2763})
    assert incidence['bfsNr'] == 2763
    assert incidence['date'] == '2021-05-04'
    assert incidence['incident'] == 318
    assert incidence['name'] == 'Arlesheim'
    assert incidence['canton'] == 'BL'
    assert incidence['area'] == 6.9
    assert incidence['population'] == 9129
    assert database.db.incidences.count_documents({}) == 3
