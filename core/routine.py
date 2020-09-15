from datetime import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.conf import settings

from requests.auth import HTTPDigestAuth


class RunJobs:
    def make_requests(self):
        print("carregando arquivos")
        requests.post(settings.URL_LOAD_FILES)


def start():
    _run_jobs = RunJobs()
    _now = datetime.now()
    scheduler = BackgroundScheduler()
    scheduler.add_job(_run_jobs.make_requests, 'interval', seconds=43200)
    scheduler.start()
