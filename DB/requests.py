from sqlalchemy import and_
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
    # Получаем пары (ID, GroupID) для всех входящих постов
    post_keys = [(post.ID, post.GroupID) for post in posts]
    # Запрос для поиска уже существующих постов с этими ключами
    existing_posts = db.query(Post.ID, Post.GroupID).filter(
        and_(Post.ID.in_([key[0] for key in post_keys]), Post.GroupID.in_([key[1] for key in post_keys]))
    ).all()
    # Преобразуем список кортежей в множество для быстрой проверки
    existing_post_keys = set(existing_posts)

    # Создаем новые посты только если их нет в базе данных
    new_posts = [
        Post(**post.dict()) for post in posts
        if (post.ID, post.GroupID) not in existing_post_keys
    ]

    if new_posts:  # Проверяем, есть ли новые посты для добавления
        db.add_all(new_posts)
        db.commit()
        for post in new_posts:
            db.refresh(post)

    return new_posts


def get_posts_by_ids(db: Session, ids: list[int]):
    return db.query(Post).filter(Post.ID.in_(ids)).all()


