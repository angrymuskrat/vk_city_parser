from sqlalchemy.orm import Session

from DB import requests
from DB.requests import create_group_if_not_exists
from api.models import UserRequestModel, TaskModel, CreateTaskModel
from master import MasterCrawler
from tasks import CollectPostsTask


def create_tasks_from_request(master: MasterCrawler, request: UserRequestModel, db: Session):
    task = CreateTaskModel(
        prompt=request.prompt,
        UserRequestID=request.ID,
        type=0,
        status=0,
        group_id=request.group_id,
        time_from=request.time_from,
        time_to=request.time_to,
    )
    created_task = requests.create_task(db, task)
    create_group_if_not_exists(db, task.group_id)
    task_for_crawler = CollectPostsTask(created_task.ID,
                                        created_task.prompt,
                                        created_task.group_id,
                                        created_task.time_from,
                                        created_task.time_to)
    master.add_request(task_for_crawler)
