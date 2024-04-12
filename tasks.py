from abc import ABC, abstractmethod


class Task(ABC):
    version = '5.199'

    def __init__(self, task_type, method_api, params):
        self.task_type = task_type
        self.method_API = method_api
        self.parameters = params
        self.response = None
        self.result = None

    @abstractmethod
    def fetch_results(self):
        pass


class CollectGroupsTask(Task):
    def fetch_results(self):
        pass

    def __init__(self, query):
        super().__init__(
            task_type='Find groups',
            method_api='https://api.vk.com/method/groups.search',
            params={'access_token': None,
                    'v': Task.version,
                    'q': str(query)}
        )


class CollectPostsTask(Task):
    def fetch_results(self):
        items = self.response['response']['items']
        for item in items:
            self.result.append(item['text'])

    def __init__(self, owner_id, count):
        super().__init__(
            task_type='Find groups',
            method_api='https://api.vk.com/method/wall.get',
            params={'access_token': None,
                    'v': Task.version,
                    'owner_id': -owner_id,
                    'count': count},
        )
        self.result = []
