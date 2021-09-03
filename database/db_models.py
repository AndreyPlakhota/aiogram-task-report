from sqlalchemy import Column, String, Integer, ForeignKey, Date
from database.database import Base


class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    e_mail = Column(String, nullable=False)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(30))
    description = Column(String(50))
    start_time = Column(String(5))
    end_time = Column(String(5))
    date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
