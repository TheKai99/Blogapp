from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base ,Session
from src.utils.settings import settings

Base = declarative_base()

engine = create_async_engine(url = settings.DB_CONNECTION)

SessionLocal = async_sessionmaker(bind = engine , expire_on_commit=False)


async def get_db():

    session = SessionLocal()

    try:
        yield session
    finally:
        await session.close()