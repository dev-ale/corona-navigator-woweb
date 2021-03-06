from app import mongo
from datascrapper import get_incidences_from_canton_services, get_municipalities_from_canton_services
import logging.config
import re

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('LOGGER')
errorLogger = logging.getLogger('ERROR-LOGGER')


# puts data from datascrapper into Database
def update_db():
    # import incidences
    logger.info("Getting data from datascrapper...")
    incidences = get_incidences_from_canton_services()
    logger.info("Iterate over cantons and incidences and save them into the database")
    for canton in incidences.values():
        for incidence in canton:
            try:
                if incidence['incidence'] is None: continue
                mongo.db.incidences.update_one(
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
                logger.info("DB Insert/Update was successful")
            except Exception as e:
                errorLogger.error('invalid data: ' + str(incidence))

    # add municipality data
    logger.info("Getting data from datascrapper...")
    municipalities = get_municipalities_from_canton_services()
    logger.info("Iterate over cantons and municipalities and save them into the database")
    for canton in municipalities.values():
        for municipality in canton:
            try:
                mongo.db.incidences.update_one(
                    {
                        'bfsNr': municipality['bfsNr'],
                    },
                    {
                        '$set': {
                            'name': re.sub(r'\s\(\w{2}\)$', '', municipality['name']),
                            'canton': municipality['canton'],
                            'area': municipality['area'],
                            'population': municipality['population']
                        }
                    }
                )
                logger.info("DB Insert/Update was successful")
            except Exception as e:
                errorLogger.error('invalid data: ' + str(municipality))
