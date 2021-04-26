import configparser
from urllib.request import urlopen
import requests
import json
import datetime
from datetime import datetime, date, timedelta
import urllib3

YESTERDAY = 1


def get_incidences_from_canton_services():
    dict = {}
    dateTo = date.today()
    dateFrom = dateTo

    # get configuration file
    parser = configparser.ConfigParser()
    parser.read("url_config.txt")

    # get data for ZH
    url_zh = parser.get("config", "zh_incidences")
    url_zh += "?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_zh)
    data = json.loads(json_url.read())
    dict['ZH'] = data

    # get data for GR
    url_gr = parser.get("config", "gr_incidences")
    url_gr += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_gr)
    data = json.loads(json_url.read())
    dict['GR'] = data

    # get data for TG
    url_tg = parser.get("config", "tg_incidences")
    url_tg += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_tg)
    data = json.loads(json_url.read())
    dict['TG'] = data

    # get data for AG
    url_ag = parser.get("config", "ag_incidences")
    url_ag += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_ag)
    data = json.loads(json_url.read())
    dict['AG'] = data

    # get data for ZG
    url_zg = parser.get("config", "zg_incidences")
    url_zg += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_zg)
    data = json.loads(json_url.read())
    dict['ZG'] = data

    # get data for BE
    url_be = parser.get("config", "be_incidences")
    url_be += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_be)
    data = json.loads(json_url.read())
    dict['BE'] = data

    # get data for SO
    url_so = parser.get("config", "so_incidences")
    url_so += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    json_url = urlopen(url_so)
    data = json.loads(json_url.read())
    dict['SO'] = data

    # get data from BS/BL
    url_blbs = parser.get("config", "blbs_incidences")
    url_blbs += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    certificate = "./certificates/certificate_blbs.pem"
    data = call_to_service_with_pool_manager(certificate, url_blbs)
    dict['BLBS'] = data

    # get data from LU
    url_lu = parser.get("config", "lu_incidences")
    url_lu += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    certificate = "./certificates/certificate_lu.pem"
    data = call_to_service_with_pool_manager(certificate, url_lu)
    dict['LU'] = data

    # get data from SZ
    url_sz = parser.get("config", "sz_incidences")
    url_sz += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    certificate = "./certificates/certificate_sz.pem"
    data = call_to_service_with_pool_manager(certificate, url_sz)
    dict['SZ'] = data

    # get data from SG
    url_sg = parser.get("config", "sg_incidences")
    url_sg += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    certificate = "./certificates/certificate_sg.pem"
    data = call_to_service_with_pool_manager(certificate, url_sg)
    dict['SG'] = data

    # get data from FR (this seems not to work due to errors in the certificate)
    url_fr = parser.get("config", "fr_incidences")
    url_fr += "/?dateFrom=" + str(dateFrom) + "&dateTo=" + str(dateTo)
    certificate = "./certificates/certificate_fr.cer"
    data = call_to_service_with_pool_manager_fr(certificate, url_fr)
    dict['FR'] = data

    return dict


def get_municipalities_from_canton_services():
    dict = {}

    # get configuration file
    parser = configparser.ConfigParser()
    parser.read("url_config.txt")

    # get data for ZH
    url_zh = parser.get("config", "zh_municipalities")
    json_url = urlopen(url_zh)
    data = json.loads(json_url.read())
    dict['ZH'] = data

    # get data for GR
    url_gr = parser.get("config", "gr_municipalities")
    json_url = urlopen(url_gr)
    data = json.loads(json_url.read())
    dict['GR'] = data

    # get data for TG
    url_tg = parser.get("config", "tg_municipalities")
    json_url = urlopen(url_tg)
    data = json.loads(json_url.read())
    dict['TG'] = data

    # get data for AG
    url_ag = parser.get("config", "ag_municipalities")
    json_url = urlopen(url_ag)
    data = json.loads(json_url.read())
    dict['AG'] = data

    # get data for ZG
    url_zg = parser.get("config", "zg_municipalities")
    json_url = urlopen(url_zg)
    data = json.loads(json_url.read())
    dict['ZG'] = data

    # get data for BE
    url_be = parser.get("config", "be_municipalities")
    json_url = urlopen(url_be)
    data = json.loads(json_url.read())
    dict['BE'] = data

    # get data for SO
    url_so = parser.get("config", "so_municipalities")
    json_url = urlopen(url_so)
    data = json.loads(json_url.read())
    dict['SO'] = data

    # get data from BS/BL
    url_blbs = parser.get("config", "blbs_municipalities")
    certificate = "./certificates/certificate_blbs.pem"
    data = call_to_service_with_pool_manager(certificate, url_blbs)
    dict['BLBS'] = data

    # get data from LU
    url_lu = parser.get("config", "lu_municipalities")
    certificate = "./certificates/certificate_lu.pem"
    data = call_to_service_with_pool_manager(certificate, url_lu)
    dict['LU'] = data

    # get data from SZ
    url_sz = parser.get("config", "sz_municipalities")
    certificate = "./certificates/certificate_sz.pem"
    data = call_to_service_with_pool_manager(certificate, url_sz)
    dict['SZ'] = data

    # get data from SG
    url_sg = parser.get("config", "sg_municipalities")
    certificate = "./certificates/certificate_sg.pem"
    data = call_to_service_with_pool_manager(certificate, url_sg)
    dict['SG'] = data

    # get data from FR (this seems not to work due to errors in the certificate)
    url_fr = parser.get("config", "fr_municipalities")
    certificate = "./certificates/certificate_fr.pem"
    data = call_to_service_with_pool_manager_fr(certificate, url_fr)
    dict['FR'] = data

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
        return []


if __name__ == '__main__':
    dict = {}
    dict['incidences'] = get_incidences_from_canton_services()
    dict['municipalities'] = get_municipalities_from_canton_services()
    print(dict)
