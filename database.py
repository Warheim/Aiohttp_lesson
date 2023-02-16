import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func

load_dotenv()

PG_DSN = f'postgresql+asyncpg://{os.getenv("PG_USER")}:{os.getenv("PG_PASSWORD")}@127.0.0.1:5431/{os.getenv("PG_DB")}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
