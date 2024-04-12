import requests

from tasks import Task


class Crawler:
    def __init__(self, token):
        self.token = token
        self.active_tasks = []
        self.completed_results = []

    def add_task(self, task):
        self.active_tasks.append(task)

    def execute_task(self, task: Task):
        params = task.parameters
        params['access_token'] = self.token
        response = requests.get(task.method_API, params, verify=False)
        data = response.json()
        task.response = data
        # Здесь будет логика выполнения задачи и возвращение результатов
        pass

    @staticmethod
    def fetch_results(task):
        if task.response is None:
            print("Error: task is not complete")
        else:
            task.fetch_results()
        # Здесь код для извлечения результатов выполненных заданий
        pass
