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
            task.make_requests(self.token, self.client, self.vectoriser)
            task.result = self.vectoriser.find_simular(task.prompt, task.response)
            task.save_in_db(db)
            update_task_status(db, task.ID, 2)
