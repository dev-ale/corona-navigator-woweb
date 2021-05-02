import configparser
from urllib.request import urlopen
import requests
import json
import datetime
from datetime import datetime, date, timedelta
import urllib3
import logging.config

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('LOGGER')
errorLogger = logging.getLogger('ERROR-LOGGER')

def get_incidences_from_canton_services():
    try:
        dict = {}
        date_to = date.today()
        date_from = date_to
        yesterday = date_to - timedelta(days=1)

        # get configuration file
        parser = configparser.ConfigParser()
        parser.read("url_config.txt")
        logger.info("Got url configuration")

        # get data for ZH
        url_zh = parser.get("config", "zh_incidences")
        url_zh += "?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        dict['ZH'] = call_to_service_without_certificate(url_zh)
        logger.info("Got data from ZH: " + str(len(dict['ZH'])) + " \t\tentries for incidences")

        # get data for GR
        url_gr = parser.get("config", "gr_incidences")
        url_gr += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        dict['GR'] = call_to_service_without_certificate(url_gr)
        logger.info("Got data from GR: " + str(len(dict['GR'])) + " \tentries for incidences")

        # get data for TG
        url_tg = parser.get("config", "tg_incidences")
        url_tg += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        dict['TG'] = call_to_service_without_certificate(url_tg)
        logger.info("Got data from TG: " + str(len(dict['TG'])) + " \t\tentries for incidences")

        # get data for AG
        url_ag = parser.get("config", "ag_incidences")
        url_ag += "/?dateFrom=" + str(yesterday) + "&dateTo=" + str(dateTo)
        dict['AG'] = call_to_service_without_certificate(url_ag)
        logger.info("Got data from AG: " + str(len(dict['AG'])) + " \t\tentries for incidences")

        # get data for ZG
        url_zg = parser.get("config", "zg_incidences")
        url_zg += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        dict['ZG'] = call_to_service_without_certificate(url_zg)
        logger.info("Got data from ZG: " + str(len(dict['ZG'])) + " \tentries for incidences")

        # get data for BE
        url_be = parser.get("config", "be_incidences")
        url_be += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        dict['BE'] = call_to_service_without_certificate(url_be)
        logger.info("Got data from BE: " + str(len(dict['BE'])) + " \tentries for incidences")

        # get data for SO
        url_so = parser.get("config", "so_incidences")
        url_so += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        dict['SO'] = call_to_service_without_certificate(url_so)
        logger.info("Got data from SO: " + str(len(dict['SO'])) + " \tentries for incidences")

        # get data from BS/BL
        url_blbs = parser.get("config", "blbs_incidences")
        url_blbs += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        certificate = "./certificates/certificate_blbs.pem"
        data = call_to_service_with_pool_manager(certificate, url_blbs)
        dict['BLBS'] = data
        logger.info("Got data from BLBS: " + str(len(dict['BLBS'])) + " \tentries for incidences")

        # get data from LU
        url_lu = parser.get("config", "lu_incidences")
        url_lu += "/?dateFrom=" + str(yesterday) + "&dateTo=" + str(date_to)
        certificate = "./certificates/certificate_lu.pem"
        data = call_to_service_with_pool_manager(certificate, url_lu)
        dict['LU'] = data
        logger.info("Got data from LU: " + str(len(dict['LU'])) + " \t\tentries for incidences")

        # get data from SZ
        url_sz = parser.get("config", "sz_incidences")
        url_sz += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        certificate = "./certificates/certificate_sz.pem"
        data = call_to_service_with_pool_manager(certificate, url_sz)
        dict['SZ'] = data
        logger.info("Got data from SZ: " + str(len(dict['SZ'])) + " \t\tentries for incidences")

        # get data from SG
        url_sg = parser.get("config", "sg_incidences")
        url_sg += "/?dateFrom=" + str(yesterday) + "&dateTo=" + str(date_to)
        certificate = "./certificates/certificate_sg.pem"
        data = call_to_service_with_pool_manager(certificate, url_sg)
        dict['SG'] = data
        logger.info("Got data from SG: " + str(len(dict['SG'])) + " \t\tentries for incidences")

        # get data from FR (this seems not to work due to errors in the certificate)
        url_fr = parser.get("config", "fr_incidences")
        url_fr += "/?dateFrom=" + str(date_from) + "&dateTo=" + str(date_to)
        certificate = "./certificates/certificate_fr.cer"
        data = call_to_service_with_pool_manager_fr(certificate, url_fr)
        dict['FR'] = data
        logger.info("Got data from FR: " + str(len(dict['FR'])) + " \tentries for incidences")

        return dict
    except Exception as ex:
        errorLogger.error(str(ex))


def get_municipalities_from_canton_services():
    dict = {}

    # get configuration file
    parser = configparser.ConfigParser()
    parser.read("url_config.txt")

    # get data for ZH
    url_zh = parser.get("config", "zh_municipalities")
    dict['ZH'] = call_to_service_without_certificate(url_zh)
    logger.info("Got data from ZH: " + str(len(dict['ZH'])) + " \tentries for municipalities")

    # get data for GR
    url_gr = parser.get("config", "gr_municipalities")
    dict['GR'] = call_to_service_without_certificate(url_gr)
    logger.info("Got data from GR: " + str(len(dict['GR'])) + " \tentries for municipalities")

    # get data for TG
    url_tg = parser.get("config", "tg_municipalities")
    dict['TG'] = call_to_service_without_certificate(url_tg)
    logger.info("Got data from TG: " + str(len(dict['TG'])) + " \t\tentries for municipalities")

    # get data for AG
    url_ag = parser.get("config", "ag_municipalities")
    dict['AG'] = call_to_service_without_certificate(url_ag)
    logger.info("Got data from AG: " + str(len(dict['AG'])) + " \tentries for municipalities")

    # get data for ZG
    url_zg = parser.get("config", "zg_municipalities")
    dict['ZG'] = call_to_service_without_certificate(url_zg)
    logger.info("Got data from ZG: " + str(len(dict['ZG'])) + " \t\tentries for municipalities")

    # get data for BE
    url_be = parser.get("config", "be_municipalities")
    dict['BE'] = call_to_service_without_certificate(url_be)
    logger.info("Got data from BE: " + str(len(dict['BE'])) + " \tentries for municipalities")

    # get data for SO
    url_so = parser.get("config", "so_municipalities")
    dict['SO'] = call_to_service_without_certificate(url_so)
    logger.info("Got data from SO: " + str(len(dict['SO'])) + " \tentries for municipalities")

    # get data from BS/BL
    url_blbs = parser.get("config", "blbs_municipalities")
    certificate = "./certificates/certificate_blbs.pem"
    data = call_to_service_with_pool_manager(certificate, url_blbs)
    dict['BLBS'] = data
    logger.info("Got data from BLBS: " + str(len(dict['BLBS'])) + " \tentries for municipalities")

    # get data from LU
    url_lu = parser.get("config", "lu_municipalities")
    certificate = "./certificates/certificate_lu.pem"
    data = call_to_service_with_pool_manager(certificate, url_lu)
    dict['LU'] = data
    logger.info("Got data from LU: " + str(len(dict['LU'])) + " \t\tentries for municipalities")

    # get data from SZ
    url_sz = parser.get("config", "sz_municipalities")
    certificate = "./certificates/certificate_sz.pem"
    data = call_to_service_with_pool_manager(certificate, url_sz)
    dict['SZ'] = data
    logger.info("Got data from SZ: " + str(len(dict['SZ'])) + " \t\tentries for municipalities")

    # get data from SG
    url_sg = parser.get("config", "sg_municipalities")
    certificate = "./certificates/certificate_sg.pem"
    data = call_to_service_with_pool_manager(certificate, url_sg)
    dict['SG'] = data
    logger.info("Got data from SG: " + str(len(dict['SG'])) + " \t\tentries for municipalities")

    # get data from FR (this seems not to work due to errors in the certificate)
    url_fr = parser.get("config", "fr_municipalities")
    certificate = "./certificates/certificate_fr.pem"
    data = call_to_service_with_pool_manager_fr(certificate, url_fr)
    dict['FR'] = data
    logger.info("Got data from FR: " + str(len(dict['FR'])) + " \tentries for municipalities")

    return dict


def call_to_service_with_pool_manager(certificate, url):
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                   ca_certs=certificate,
                                   assert_hostname=False)
        r = http.request('GET', url)
        json_data = r.data.decode('utf-8')
        data = json.loads(json_data)
        return data
    except Exception as ex:
        errorLogger.error(str(ex))
        return []


def call_to_service_with_pool_manager_fr(certificate, url):
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_NONE',
                                   ca_certs=certificate,
                                   assert_hostname=False)
        r = http.request('GET', url)
        json_data = r.data.decode('utf-8')
        data = json.loads(json_data)
        return data
    except Exception as ex:
        errorLogger.error(str(ex))
        return []

def call_to_service_without_certificate(url):
    try:
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        return data
    except Exception as ex:
        errorLogger.error(str(ex))
        return []


if __name__ == '__main__':
    dict = {}
    dict['incidences'] = get_incidences_from_canton_services()
    dict['municipalities'] = get_municipalities_from_canton_services()
