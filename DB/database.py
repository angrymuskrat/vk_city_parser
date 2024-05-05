from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Замените 'postgresql://username:password@localhost/dbname' на ваше подключение к PostgreSQL.
DATABASE_URL = 'postgresql+asyncpg://postgres:example@localhost:4321/postgres'

# Создание объекта Engine для работы с базой данных
engine = create_async_engine(DATABASE_URL)

# Создание сессии базы данных
SessionLocal = sessionmaker(expire_on_commit=False,
                            autocommit=False,
                            autoflush=False,
                            class_=AsyncSession,
                            bind=engine)

# Создание базового класса моделей
Base = declarative_base()
