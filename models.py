from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registration_date = Column(DateTime, server_default=func.now())
