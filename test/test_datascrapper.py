from datascrapper import *

incidence_response = [{
    'bfsNr': 1,
    'date': '2021-05-15',
    'incidence': 123
}]

municipalitiy_response = [{
    'area': 7.4,
    'bfsNr': 2761,
    'canton': 'BL',
    'name': 'Aesch',
    'population': 10352
}]

def test_get_incidences_from_canton_services(mocker):
    mocker.patch('datascrapper.call_to_service_with_pool_manager', return_value=incidence_response)
    mocker.patch('datascrapper.call_to_service_without_certificate', return_value=incidence_response)
    mocker.patch('datascrapper.call_to_service_with_pool_manager_fr', return_value=incidence_response)
    incidences = get_incidences_from_canton_services()
    assert incidences['SO'] == incidence_response
    assert sorted(incidences.keys()) == [
        'AG',
        'BE',
        'BLBS',
        'FR',
        'GR',
        'LU',
        'SG',
        'SO',
        'SZ',
        'TG',
        'ZG',
        'ZH'
    ]

def test_get_municipalities_from_canton_services(mocker):
    mocker.patch('datascrapper.call_to_service_with_pool_manager', return_value=municipalitiy_response)
    mocker.patch('datascrapper.call_to_service_without_certificate', return_value=municipalitiy_response)
    mocker.patch('datascrapper.call_to_service_with_pool_manager_fr', return_value=municipalitiy_response)
    municipalities = get_municipalities_from_canton_services()
    assert municipalities['SO'] == municipalitiy_response
    assert sorted(municipalities.keys()) == [
        'AG',
        'BE',
        'BLBS',
        'FR',
        'GR',
        'LU',
        'SG',
        'SO',
        'SZ',
        'TG',
        'ZG',
        'ZH'
    ]
