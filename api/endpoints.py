from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from DB import requests
from DB.database import SessionLocal
from api.models import UserRequestModel

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/user_requests/{user_request_id}", response_model=UserRequestModel)
def read_user_request(user_request_id: int, db: Session = Depends(get_db)):
    db_user_request = requests.get_user_request(db, user_request_id=user_request_id)
    if db_user_request is None:
        raise HTTPException(status_code=404, detail="UserRequest not found")
    return db_user_request


@app.post("/user_requests/", response_model=UserRequestModel, status_code=status.HTTP_201_CREATED)
def create_user_request_endpoint(user_request: UserRequestModel, db: Session = Depends(get_db)):
    return requests.create_user_request(db=db, user_request=user_request)
