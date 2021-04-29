from app import mongo
from datascrapper import get_incidences_from_canton_services, get_municipalities_from_canton_services

#puts data from datascraper into Database
def update_db():
    # import incidences
    incidences = get_incidences_from_canton_services()
    for canton in incidences.values():
        for incidence in canton:
            try:
                mongo.db.incidences.update(
                    {
                        'bfsNr': incidence['bfsNr'],
                    },
                    {
                        '$set': {
                            'bfsNr': incidence['bfsNr'],
                            'date': incidence['date'],
                            'incident': incidence['incidence']
                        }
                    },
                    upsert=True
                )
            except Exception as e:
                print('invalid data: ' + str(incidence)) # TODO add logger

    # add municipality data
    municipalities = get_municipalities_from_canton_services()
    for canton in municipalities.values():
        for municipality in canton:
            try:
                mongo.db.incidences.update(
                    {
                        'bfsNr': municipality['bfsNr'],
                    },
                    {
                        '$set': {
                            'name': municipality['name'],
                            'canton': municipality['canton'],
                            'area': municipality['area'],
                            'population': municipality['population']
                        }
                    }
                )
            except Exception as e:
                print('invalid data: ' + str(municipality)) # TODO add logger
