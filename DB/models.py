from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

post_task_table = Table('post_task', Base.metadata,
                        Column('PostID', Integer, ForeignKey('post.ID')),
                        Column('TaskID', Integer, ForeignKey('task.ID'))
                        )

group_task_table = Table('group_task', Base.metadata,
                         Column('GroupID', Integer, ForeignKey('group.ID')),
                         Column('TaskID', Integer, ForeignKey('task.ID'))
                         )


class UserRequest(Base):
    __tablename__ = 'user_request'

    ID = Column(Integer, primary_key=True)
    prompt = Column(String(255))
    type = Column(Integer)
    status = Column(Integer)
    # group_id = Column(Integer, ForeignKey('group.ID'))
    time_from = Column(DateTime)
    time_to = Column(DateTime)

    # group = relationship("Group", back_populates="user_requests")
    tasks = relationship("Task", back_populates="user_request")


class Task(Base):
    __tablename__ = 'task'

    ID = Column(Integer, primary_key=True)
    UserRequestID = Column(Integer, ForeignKey('user_request.ID'))
    prompt = Column(String(255))
    type = Column(String(255))
    # group_id = Column(Integer, ForeignKey('group.ID'))
    time_from = Column(DateTime)
    time_to = Column(DateTime)

    user_request = relationship("UserRequest", back_populates="tasks")
    groups = relationship("Group", secondary=group_task_table, back_populates="task")
    posts = relationship("Post", secondary=post_task_table, back_populates="task")


class Group(Base):
    __tablename__ = 'group'

    ID = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    vector = Column(Float)

    # user_requests = relationship("UserRequest", back_populates="group")
    posts = relationship("Post", back_populates="group")
    task = relationship("Task", secondary=group_task_table, back_populates="groups")


class Post(Base):
    __tablename__ = 'post'

    ID = Column(Integer, primary_key=True)
    text = Column(String(255))
    GroupID = Column(Integer, ForeignKey('group.ID'))
    vector = Column(Float)

    group = relationship("Group", back_populates="posts")
    task = relationship("Task", secondary=post_task_table, back_populates="posts")
