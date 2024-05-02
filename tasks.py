from datetime import datetime

from sqlalchemy.orm import Session

from DB.requests import create_posts, add_task_to_multiple_posts
from api.models import PostModel
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

    def fetch_results(self, response: dict, vectorizer: TextVectorizer) -> bool:
        pass

    def save_in_db(self, db: Session):
        pass


class CollectGroupsTask(Task):
    def fetch_results(self, response: dict, vectorizer: TextVectorizer) -> bool:
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

    def fetch_results(self, response, vectorizer: TextVectorizer) -> bool:
        # print(response)
        items = response['response']['items']
        for item in items:
            date = datetime.fromtimestamp(item['date'])
            if self.date_from <= date.date() <= self.date_to:
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
            # print(result['vector'].tolist())
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

