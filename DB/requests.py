from sqlalchemy import and_
from sqlalchemy.orm import Session
from DB.models import UserRequest, Post, Task, Group
from api.models import UserRequestModel, PostModel, TaskModel, CreateUserRequestModel, CreateTaskModel


def get_user_request(db: Session, user_request_id: int) -> UserRequestModel:
    return db.query(UserRequest).filter(UserRequest.ID == user_request_id).first()


def create_user_request(db: Session, user_request: CreateUserRequestModel):
    db_user_request = UserRequest(**user_request.dict(exclude_unset=True))
    db.add(db_user_request)
    db.commit()
    db.refresh(db_user_request)
    return db_user_request


def create_task(db: Session, task: CreateTaskModel):
    db_task = Task(**task.dict(exclude_unset=True))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task_status(db: Session, task_id: int, new_status: int):
    task = db.query(Task).filter(Task.ID == task_id).first()
    if not task:
        return None
    task.status = new_status
    db.commit()
    return task


def get_task_statuses_by_user_request_id(db: Session, user_request_id: int):
    tasks = db.query(Task).join(UserRequest).filter(UserRequest.ID == user_request_id).all()
    task_statuses = [(task.ID, task.status) for task in tasks]
    return task_statuses


def create_group_if_not_exists(db: Session, group_id: int):
    existing_group = db.query(Group).filter(Group.ID == group_id).first()
    if existing_group is not None:
        return existing_group

    new_group = Group(ID=group_id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def create_posts(db: Session, posts: list[PostModel]):
    post_keys = [(post.ID, post.GroupID) for post in posts]
    existing_posts = db.query(Post.ID, Post.GroupID).filter(
        and_(Post.ID.in_([key[0] for key in post_keys]), Post.GroupID.in_([key[1] for key in post_keys]))
    ).all()
    existing_post_keys = set(existing_posts)

    new_posts = [
        Post(**post.dict()) for post in posts
        if (post.ID, post.GroupID) not in existing_post_keys
    ]

    if new_posts:
        db.add_all(new_posts)
        db.commit()
        for post in new_posts:
            db.refresh(post)

    return new_posts


def get_posts_by_ids(db: Session, post_ids: list[int], group_id: int,):
    return db.query(Post).filter(Post.GroupID == group_id, Post.ID.in_(post_ids)).all()


def get_group_posts_by_task_id(db: Session, task_id: int):
    # Получаем все посты и их группы, связанные с задачей по её ID
    results = db.query(Group.name, Post.text) \
        .join(Post, Group.posts) \
        .join(Task, Post.task) \
        .filter(Task.ID == task_id) \
        .all()

    if not results:
        return None  # Возвращаем None, если по задаче нет постов или группы

    # Используем имя группы как ключ, и собираем список постов как значения
    group_name = results[0][0]  # Предполагаем, что все посты из одной группы
    posts = [post_text for _, post_text in results]

    # Формируем словарь с именем группы и списком постов
    group_posts = {group_name: posts}

    return group_posts


def add_task_to_multiple_posts(db: Session, post_ids: list[int], group_id: int, task_id: int):
    task = db.query(Task).filter(Task.ID == task_id).first()
    if not task:
        return "Task not found"

    posts = db.query(Post).filter(Post.GroupID == group_id, Post.ID.in_(post_ids)).all()
    if not posts:
        return "No posts found"

    for post in posts:
        if post not in task.posts:
            task.posts.append(post)

    db.commit()
    db.refresh(task)
    return task
