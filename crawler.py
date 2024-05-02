import json
import threading
from time import sleep

from DB.database import SessionLocal
from DB.requests import update_task_status
from HttpClient import HttpClient
from tasks import Task
from vectorizer import TextVectorizer


class Crawler:

    def __init__(self, id: int, token: str):
        self.id = id
        self.vectoriser = TextVectorizer()
        self.client = HttpClient()
        self.token = token
        self.status = 'free'
        self.task: Task = None
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            # print("my id:", self.id, "my status:", self.status)
            if self.status != "done":
                if self.task is not None:
                    self.execute_task()
                    self.status = "done"
            sleep(0.5)

    def execute_task(self):
        with SessionLocal() as db:
            task = self.task
            update_task_status(db, task.ID, 1)
            params = task.parameters
            params['access_token'] = self.token
            while True:
                data = self.client.get_request(task.method_API, params)
                # pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
                # print(pretty_json)
                if not task.fetch_results(data, self.vectoriser):
                    break
                params['offset'] += params['count']
                print("my id:", self.id, "my response:", self.task.response)
            task.result = self.vectoriser.find_simular(task.prompt, task.response)
            task.save_in_db(db)
            update_task_status(db, task.ID, 2)
