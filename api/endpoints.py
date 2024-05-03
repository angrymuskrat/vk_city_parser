from fastapi import HTTPException, Depends, status, FastAPI
from sqlalchemy.orm import Session

from DB import requests
from DB.database import SessionLocal
from api.models import UserRequestModel, CreateUserRequestModel, AnswerUserRequestModel, CreateTaskModel, TaskModel
from logic.request_to_tasks import create_tasks_from_request, check_status_of_user_request
from master import MasterCrawler
from tasks import CollectGroupsTask

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


token = 'vk1.a.N0Bo0jedRrOsPYno8fHywsFSKG2FuAJoO1az6snThQqDl6AwwseVhdlhDITyYjEUjqFvqHAqbvGocmgNo2laOPrO-YXRGo8o10PVV2bFLXtFfD0SowoIoDY32pdVXNGB7BOFE2W3ZUYWqHbOTPYO7eBNuHHid1EwCP2ttaV1B8U5qMkqdGQ6eeut1lF8GYnTWwgAUfcL29Mg3aycsAZktw'

master_crawler = MasterCrawler(1, [token])


@app.get("/user_requests/{user_request_id}", response_model=AnswerUserRequestModel)
def read_user_request(user_request_id: int, db: Session = Depends(get_db)):
    db_user_request = requests.get_user_request(db, user_request_id=user_request_id)
    if db_user_request is None:
        raise HTTPException(status_code=404, detail="UserRequest not found")
    answer_user_request = check_status_of_user_request(db_user_request, db)
    return answer_user_request


@app.post("/user_requests/", response_model=UserRequestModel, status_code=status.HTTP_201_CREATED)
def create_user_request_endpoint(user_request: CreateUserRequestModel, db: Session = Depends(get_db)):
    ret = requests.create_user_request(db=db, user_request=user_request)
    create_tasks_from_request(master_crawler, ret, db)
    return ret


@app.post("/add_groups/", response_model=TaskModel, status_code=status.HTTP_201_CREATED)
def create_groups(user_request: CreateTaskModel, db: Session = Depends(get_db)):
    created_task = requests.create_task(db, user_request)
    task_for_crawler = CollectGroupsTask(created_task.ID,
                                         created_task.prompt)
    master_crawler.add_request(task_for_crawler)
    return created_task
