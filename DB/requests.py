from sqlalchemy.orm import Session
from DB.models import UserRequest, Post
from api.models import UserRequestModel, PostModel


def get_user_request(db: Session, user_request_id: int):
    return db.query(UserRequest).filter(UserRequest.ID == user_request_id).first()


def create_user_request(db: Session, user_request: UserRequestModel):
    db_user_request = UserRequest(**user_request.dict())
    db.add(db_user_request)
    db.commit()
    db.refresh(db_user_request)
    return db_user_request


def create_posts(db: Session, posts: list[PostModel]):
    db_posts = [Post(**post.dict()) for post in posts]
    db.add_all(db_posts)
    db.commit()
    for post in db_posts:
        db.refresh(post)
    return db_posts


def get_posts_by_ids(db: Session, ids: list[int]):
    return db.query(Post).filter(Post.ID.in_(ids)).all()


