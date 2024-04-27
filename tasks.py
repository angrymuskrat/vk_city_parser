from datetime import datetime


class Task:
    version = '5.199'

    def __init__(self, id: int, prompt: str, task_type: str, method_api: str, params: dict):
        self.ID = id
        self.prompt = prompt
        self.task_type = task_type
        self.method_API = method_api
        self.parameters = params
        self.response = None
        self.result = None

    def fetch_results(self, response: dict) -> bool:
        pass


class CollectGroupsTask(Task):
    def fetch_results(self, response: dict) -> bool:
        pass

    def __init__(self, query: str):
        super().__init__(
            prompt=query,
            task_type='Find groups',
            method_api='https://api.vk.com/method/groups.search',
            params={'access_token': None,
                    'offset': 0,
                    'v': Task.version,
                    'q': str(query)}
        )


class CollectPostsTask(Task):
    count = 100

    def __init__(self, id: int, prompt: str, owner_id: int, date_from: str, date_to: str):
        super().__init__(
            id=id,
            prompt=prompt,
            task_type='Find groups',
            method_api='https://api.vk.com/method/wall.get',
            params={'access_token': None,
                    'offset': 0,
                    'v': Task.version,
                    'owner_id': -owner_id,
                    'count': CollectPostsTask.count},
        )
        self.response = []
        self.date_from = datetime.strptime(date_from, '%d.%m.%Y')
        self.date_to = datetime.strptime(date_to, '%d.%m.%Y')

    def fetch_results(self, response) -> bool:
        #print(response)
        items = response['response']['items']
        for item in items:
            date = datetime.fromtimestamp(item['date'])
            if self.date_from <= date <= self.date_to:
                self.response.append(item['text'])
        if datetime.fromtimestamp(items[-1]['date']) > self.date_from:
            return True
        return False
