
class Task:
    version = '5.199'

    def __init__(self, prompt, task_type, method_api, params):
        self.prompt = prompt
        self.task_type = task_type
        self.method_API = method_api
        self.parameters = params
        self.response = None
        self.result = None

    def fetch_results(self, response):
        pass


class CollectGroupsTask(Task):
    def fetch_results(self, response):
        pass

    def __init__(self, query):
        super().__init__(
            prompt=query,
            task_type='Find groups',
            method_api='https://api.vk.com/method/groups.search',
            params={'access_token': None,
                    'v': Task.version,
                    'q': str(query)}
        )


class CollectPostsTask(Task):
    def __init__(self, prompt, owner_id, count):
        super().__init__(
            prompt=prompt,
            task_type='Find groups',
            method_api='https://api.vk.com/method/wall.get',
            params={'access_token': None,
                    'v': Task.version,
                    'owner_id': -owner_id,
                    'count': count},
        )
        self.response = []

    def fetch_results(self, response):
        items = response['response']['items']
        for item in items:
            self.response.append(item['text'])
