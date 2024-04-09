class Crawler:
    def __init__(self, token):
        self.token = token
        self.active_tasks = []
        self.completed_results = []

    def add_task(self, task):
        self.active_tasks.append(task)

    def execute_task(self, task):
        # Здесь будет логика выполнения задачи и возвращение результатов
        pass

    def fetch_results(self):
        # Здесь код для извлечения результатов выполненных заданий
        pass
