import os
from dotenv import load_dotenv

load_dotenv()

PG_DSN = f'postgresql+asyncpg://{os.getenv("PG_USER")}:{os.getenv("PG_PASSWORD")}@127.0.0.1:5431/{os.getenv("PG_DB")}'
