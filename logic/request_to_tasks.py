from sqlalchemy.orm import Session

from DB import requests
from DB.requests import create_group_if_not_exists, get_task_statuses_by_user_request_id, get_group_posts_by_task_id
from api.models import UserRequestModel, CreateTaskModel, AnswerUserRequestModel
from master import MasterCrawler
from tasks import CollectPostsTask


def check_status_of_user_request(user_request: UserRequestModel, db: Session) -> AnswerUserRequestModel:
    statuses = get_task_statuses_by_user_request_id(db, user_request.ID)
    tasks_count = len(statuses)
    task_in_process_count = sum(1 for _, status in statuses if status == 1)
    task_done_count = sum(1 for _, status in statuses if status == 2)
    status = 0
    posts = None
    if task_in_process_count > 0:
        status = 1
    if tasks_count == task_done_count:
        status = 2
        posts = {}
        for task_id, _ in statuses:
            task_posts = get_group_posts_by_task_id(db, task_id)
            posts.update(task_posts)

    answer = AnswerUserRequestModel(
        ID=user_request.ID,
        prompt=user_request.prompt,
        status=status,
        tasks_count=tasks_count,
        tasks_in_process=task_in_process_count,
        tasks_done=task_done_count,
        time_from=user_request.time_from,
        time_to=user_request.time_to,
        answer=posts,
    )
    return answer


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
