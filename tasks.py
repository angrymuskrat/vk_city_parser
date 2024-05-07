from datetime import datetime

from sqlalchemy.orm import Session

import HttpClient
from DB.requests import create_posts, add_task_to_multiple_posts, create_or_update_groups, add_task_to_multiple_groups
from api.models import PostModel, GroupModel
from vectorizer import TextVectorizer


class Task:
    version = '5.199'

    def __init__(self, id: int, prompt: str, task_type: str, method_api: str, params: dict):
        self.ID = id
        self.prompt = prompt
        self.task_type = task_type
        self.method_API = method_api
        self.parameters = params
        self.response: list[dict] = None
        self.result: list[dict] = None

    def make_requests(self, token: str, client: HttpClient, vectorizer: TextVectorizer):
        pass

    def save_in_db(self, db: Session):
        pass


class CollectGroupsTask(Task):
    city_id = 2  # SPB
    count = 10
    find_group_description_api = 'https://api.vk.com/method/execute'

    def __init__(self, id: int, query: str):
        super().__init__(
            id=id,
            prompt=query,
            task_type='Find groups',
            method_api='https://api.vk.com/method/groups.search',
            params={'access_token': None,
                    'offset': 0,
                    'city_id': CollectGroupsTask.city_id,
                    'count': CollectGroupsTask.count,
                    'v': Task.version,
                    'q': str(query)}
        )
        self.response = []

    def make_requests(self, token: str, client: HttpClient, vectorizer: TextVectorizer):
        self.parameters['access_token'] = token
        data = client.get_request(self.method_API, self.parameters)
        items = data['response']['items']
        group_ids = [item['id'] for item in items]
        descriptions = self.find_descriptions(group_ids, token, client)
        for i, item in enumerate(items):
            group_id = item['id']
            group_name = item['name']
            description = descriptions[i]
            my_dict = {
                'id': group_id,
                'name': group_name,
                'text': description,
                'vector': vectorizer.vectorize(group_name + description)
            }
            self.response.append(my_dict)

    @staticmethod
    def find_descriptions(group_ids: list[int], token: str, client: HttpClient) -> list[str]:
        code = "return {"
        for i in range(len(group_ids)):
            code += f"group{i}: API.groups.getById({{'group_id': {group_ids[i]}, 'fields': 'description'}}), "
        code += "};"
        params = {'access_token': token,
                  'code': code,
                  'v': Task.version
                  }
        data = client.get_request(CollectGroupsTask.find_group_description_api, params)
        groups_data = data['response']
        descriptions = []
        for group_key in groups_data:
            group_info = groups_data[group_key]['groups']
            for group in group_info:
                description = group['description']
                descriptions.append(description)
        return descriptions

    def save_in_db(self, db: Session):
        groups = []
        for result in self.response:
            group = GroupModel(
                ID=result.get('id'),
                name=result.get('name'),
                description=result.get('text'),
                vector=result.get('vector').tolist()
            )
            groups.append(group)
        create_or_update_groups(db, groups)

        group_ids = []
        for result in self.result:
            group_ids.append(result.get('id'))
        add_task_to_multiple_groups(db, group_ids, self.ID)


class CollectPostsTask(Task):
    count = 100

    def __init__(self, id: int, prompt: str, owner_id: int, date_from: datetime.date, date_to: datetime.date):
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
        self.group_id = owner_id
        self.response = []
        self.date_from = date_from
        self.date_to = date_to

    def make_requests(self, token: str, client: HttpClient, vectorizer: TextVectorizer):
        self.parameters['access_token'] = token
        while True:
            data = client.get_request(self.method_API, self.parameters)
            if not self.fetch_results(data, vectorizer):
                break
            self.parameters['offset'] += self.parameters['count']

    def fetch_results(self, response, vectorizer: TextVectorizer) -> bool:
        items = response['response']['items']
        for item in items:
            date = datetime.fromtimestamp(item['date'])
            if self.date_from <= date.date() <= self.date_to:
                if item['text'] != "":
                    my_dict = {'id': item['id'],
                               'date': date,
                               'text': item['text'],
                               'vector': vectorizer.vectorize(item['text'])
                               }
                    self.response.append(my_dict)
        if datetime.fromtimestamp(items[-1]['date']).date() > self.date_from:
            return True
        return False

    def save_in_db(self, db: Session):
        posts = []
        for result in self.response:
            post = PostModel(
                ID=result['id'],
                text=result['text'],
                GroupID=self.group_id,
                date=result['date'].date(),
                vector=result['vector'].tolist()
            )
            posts.append(post)
        create_posts(db, posts)

        post_ids = []
        for result in self.result:
            post_ids.append(result.get('id'))
        add_task_to_multiple_posts(db, post_ids, self.group_id, self.ID)
