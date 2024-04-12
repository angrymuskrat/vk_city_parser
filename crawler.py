import json
import threading

import requests

from HttpClient import HttpClient
from tasks import Task
from vectorizer import TextVectorizer


class Crawler:

    def __init__(self, token: str):
        self.vectoriser = TextVectorizer()
        self.client = HttpClient()
        self.token = token
        self.status = 'free'
        self.task = None
        self.thread = threading.Thread(target=self.execute_task())
        self.thread.daemon = True
        self.thread.start()

    def execute_task(self):
        task = self.task
        params = task.parameters
        params['access_token'] = self.token
        data = self.client.get_request(task.method_API, params)
        #pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
        #print(pretty_json)
        task.fetch_results(data)
        self.vectoriser.find_simular(task.prompt, task.response)
