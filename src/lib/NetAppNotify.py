import time
import json
import requests
import queue
import threading
import shutil
import os
import pytz
from datetime import datetime
from requests.auth import HTTPBasicAuth
from NetAppApiConfig import Config

class Notify (threading.Thread):

    def __init__(self, log='', config={}, kpi_timers={}):
        threading.Thread.__init__(self)
        self.log = log
        self.config = config
        self.kpi_timers = kpi_timers
        self.q = queue.Queue()
        self.log.debug(Config.LOG_NOTIFY, "Init thread")

    def run(self):

        self.log.debug(Config.LOG_NOTIFY, "Processing queue")
        while True:
            item = self.q.get()
            self.log.debug(Config.LOG_NOTIFY, "Item in queue")
            self.log.debug(Config.LOG_NOTIFY, f'{item}')

            data = item[0]
            external_id = item[1]
            json_data = item[2]
            
            self.notifyMN(data, external_id, json_data)

            self.q.task_done()

    def notifyMN(self, data, external_id, kpi_hash):

        try:

            headers = {}
            headers["Authorization"] = "Bearer " + self.config.MN_TOKEN

            self.log.debug(Config.LOG_NOTIFY, "Notifying MN at " + self.config.MN_HOST + ": " + external_id + ", " + json.dumps(data))
            r = requests.post(self.config.MN_HOST + "/api/update_agent_nef_status/" + requests.utils.quote(external_id), headers=headers, data=json.dumps(data))
            self.log.debug(Config.LOG_NOTIFY, str(r.text))

            # KPI measurement, vertical succesfully responses 
            if r.status_code == 200 and kpi_hash in self.kpi_timers:

                kpi_diff = int(time.time() * 1000)-self.kpi_timers[kpi_hash]
                self.log.debug(Config.LOG_NOTIFY, 'KPI: ' + str(kpi_diff)+'ms' + ' - ' + str(data))
                # Delete from dict of KPI hash
                del self.kpi_timers[kpi_hash]


        except Exception as e:
            self.log.error(Config.LOG_NOTIFY, str(e))
