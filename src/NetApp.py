import time
import json
import requests
import socket
import threading
import os
from NetAppApiConfig import Config
from lib.NetAppLog import NetAppLog
from lib.NetAppApiServer import ApiServer
from lib.NetAppApiClient import ApiClient
from requests.auth import HTTPBasicAuth
from multiprocessing import Process
from aiohttp import web
from optparse import OptionParser

if __name__ == '__main__':

    # Parse options
    parser = OptionParser()
    parser.add_option("-n", action="store", dest="NET_APP_NAME", help="Net application name", default=Config.NET_APP_NAME)
    parser.add_option("-t", action="store", dest="NET_API_PROT", help="Net API protocol", default=Config.NET_API_PROT)
    parser.add_option("-s", action="store", dest="NET_API_ADDRESS", help="Net API address", default=Config.NET_API_ADDRESS)
    parser.add_option("-U", action="store", dest="NET_API_USER", help="Net API user", default=Config.NET_API_USER)
    parser.add_option("-P", action="store", dest="NET_API_PASS", help="Net API pass", default=Config.NET_API_PASS)
    parser.add_option("-c", action="store", dest="CALLBACK_ADDRESS", help="Callback address", default=Config.CALLBACK_ADDRESS)
    parser.add_option("-q", action="store", dest="COLLECTOR_HOST", help="Collector host", default=Config.COLLECTOR_HOST)
    parser.add_option("-o", action="store", dest="COLLECTOR_USER", help="Collector user", default=Config.COLLECTOR_USER)
    parser.add_option("-r", action="store", dest="COLLECTOR_PASS", help="Collector pass", default=Config.COLLECTOR_PASS)
    parser.add_option("-z", action="store", dest="MN_HOST", help="MN host", default=Config.MN_HOST)
    parser.add_option("-Z", action="store", dest="MN_TOKEN", help="MN token", default=Config.MN_TOKEN)
    parser.add_option("-C", action="store", dest="CAPIF_PATH", help="CAPIF PATH", default=Config.CAPIF_PATH)
    parser.add_option("-m", action="store", dest="CAPIF_HOSTNAME", help="CAPIF hostname", default=Config.CAPIF_HOSTNAME)
    parser.add_option("-p", action="store", dest="CAPIF_PORT_HTTP", help="CAPIF HTTP port", default=Config.CAPIF_PORT_HTTP)
    parser.add_option("-S", action="store", dest="CAPIF_PORT_HTTPS", help="CAPIF HTTPS port", default=Config.CAPIF_PORT_HTTPS)
    parser.add_option("-u", action="store", dest="CAPIF_CALLBACK_ADDRESS", help="CAPIF Callback address", default=Config.CAPIF_CALLBACK_ADDRESS)
    parser.add_option("-e", action="store", dest="ENDPOINT_TEST", help="Endpoint test flag", default=Config.ENDPOINT_TEST)
    parser.add_option("-E", action="store", dest="ENVIRONMENT_MODE", help="Environmental mode", default=Config.ENVIRONMENT_MODE)

    (options, args) = parser.parse_args()

    # Save options to config file
    config = options

    # Check Endpoint flag
    if config.ENDPOINT_TEST in ['true', 'True', True]:
        config.ENDPOINT_TEST = True
    else:
        config.ENDPOINT_TEST = False   

    print(config)

    netapplogger = NetAppLog(netapp_name=config.NET_APP_NAME)
    netapplogger.debug('NetApp starting ...')

    # Start API server
    apiServer = ApiServer(netapplogger, config)
    result_server = apiServer.runServer()

    if result_server == False:
        netapplogger.debug('Exiting ... NetApp API Server not OK!')
        os._exit(1)
