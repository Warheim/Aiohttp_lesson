from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import PG_DSN

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
