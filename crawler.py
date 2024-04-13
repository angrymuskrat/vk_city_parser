import json
import threading
from time import sleep

from HttpClient import HttpClient
from vectorizer import TextVectorizer


class Crawler:

    def __init__(self, id: int, token: str):
        self.id = id
        self.vectoriser = TextVectorizer()
        self.client = HttpClient()
        self.token = token
        self.status = 'free'
        self.task = None
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            print("my id:", self.id, "my status:", self.status)
            if self.status != "done":
                if self.task is not None:
                    self.execute_task()
                    self.status = "done"
            sleep(0.5)

    def execute_task(self):
        task = self.task
        params = task.parameters
        params['access_token'] = self.token
        data = self.client.get_request(task.method_API, params)
        # pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
        # print(pretty_json)
        task.fetch_results(data)
        print("my id:", self.id, "my response:", self.task.response)
        task.result = self.vectoriser.find_simular(task.prompt, task.response)
