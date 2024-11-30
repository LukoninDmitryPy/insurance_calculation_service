from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import PG 

# set url for db
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{PG['user']}:{PG['pass']}@{PG['host']}:{PG['port']}/{PG['database']}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
