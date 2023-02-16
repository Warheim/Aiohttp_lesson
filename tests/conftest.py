import pytest
import os
from dotenv import load_dotenv
from models import Base, UserModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

PG_DSN = f'postgresql+psycopg2://{os.getenv("PG_USER")}:{os.getenv("PG_PASSWORD")}@127.0.0.1:5431/{os.getenv("PG_DB")}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope='session', autouse=True)
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def create_user():
    with Session() as session:
        new_user = UserModel(name=f'{datetime.now()}', password='120290')
        session.add(new_user)
        session.commit()
        return {'id': new_user.id, 'name': new_user.name, 'password': new_user.password}
