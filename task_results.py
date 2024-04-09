class TaskResult:
    def __init__(self, task, result=None, error_message=None):
        self.task = task
        self.result = result
        self.error_message = error_message
