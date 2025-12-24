import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "doctoroil")
    DB_USER = os.getenv("DB_USER", "oiladmin2025")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "clmtdoctoroil6388")

    DATABASE_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,      # 연결이 살아있는지 먼저 확인 (매우 중요!)
    pool_recycle=3600,       # 1시간마다 연결 재활용
    pool_size=10,            # 기본 커넥션 수
    max_overflow=20          # 최대 추가 가능 커넥션 수
)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session

        finally:
            await session.close()
