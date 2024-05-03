from sqlalchemy import Column, Integer, String, Table, ForeignKey, ARRAY, Date, TEXT, PrimaryKeyConstraint, \
    ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from DB.vector import Vector

Base = declarative_base()

post_task_table = Table('post_task', Base.metadata,
                        Column('PostID', Integer),
                        Column('GroupID', Integer),
                        Column('TaskID', Integer, ForeignKey('task.ID')),
                        PrimaryKeyConstraint('PostID', 'GroupID', 'TaskID'),
                        ForeignKeyConstraint(['PostID', 'GroupID'], ['post.ID', 'post.GroupID'])
                        )

group_task_table = Table('group_task', Base.metadata,
                         Column('GroupID', Integer, ForeignKey('group.ID')),
                         Column('TaskID', Integer, ForeignKey('task.ID')),
                         PrimaryKeyConstraint('GroupID', 'TaskID')
                         )


class UserRequest(Base):
    __tablename__ = 'user_request'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    prompt = Column(TEXT)
    type = Column(Integer, default=0)
    status = Column(Integer, default=0)
    group_id = Column(ARRAY(Integer), nullable=True)
    time_from = Column(Date, nullable=True)
    time_to = Column(Date, nullable=True)

    # group = relationship("Group", back_populates="user_requests")
    tasks = relationship("Task", back_populates="user_request")


class Task(Base):
    __tablename__ = 'task'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserRequestID = Column(Integer, ForeignKey('user_request.ID'))
    prompt = Column(TEXT)
    type = Column(Integer)
    status = Column(Integer, default=0)
    group_id = Column(Integer, nullable=True)
    time_from = Column(Date, nullable=True)
    time_to = Column(Date, nullable=True)

    user_request = relationship("UserRequest", back_populates="tasks")
    groups = relationship("Group", secondary=group_task_table, back_populates="task")
    posts = relationship("Post", secondary=post_task_table, back_populates="task")


class Group(Base):
    __tablename__ = 'group'

    ID = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    description = Column(TEXT, nullable=True)
    vector = Column(Vector, nullable=True)

    # user_requests = relationship("UserRequest", back_populates="group")
    posts = relationship("Post", back_populates="group")
    task = relationship("Task", secondary=group_task_table, back_populates="groups")


class Post(Base):
    __tablename__ = 'post'

    ID = Column(Integer, primary_key=True)
    GroupID = Column(Integer, ForeignKey('group.ID'), primary_key=True)
    text = Column(TEXT)
    date = Column(Date)
    vector = Column(Vector)

    group = relationship("Group", back_populates="posts")
    task = relationship("Task", secondary=post_task_table, back_populates="posts")
