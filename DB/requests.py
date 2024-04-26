from sqlalchemy.orm import Session
from DB.models import UserRequest
from api.models import UserRequestModel


def get_user_request(db: Session, user_request_id: int):
    return db.query(UserRequest).filter(UserRequest.ID == user_request_id).first()


def create_user_request(db: Session, user_request: UserRequestModel):
    db_user_request = UserRequest(**user_request.dict())
    db.add(db_user_request)
    db.commit()
    db.refresh(db_user_request)
    return db_user_request
