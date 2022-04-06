from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings


sqlalchemy_database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    port=settings.POSTGRES_PORT,
    host=settings.DB_HOST,
    path=f"/{settings.POSTGRES_DB}",
)

engine = create_async_engine(sqlalchemy_database_uri)
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
