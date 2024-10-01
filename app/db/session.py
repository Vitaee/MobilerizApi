from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.SQLALCHEMY_DATABASE_URI else {}
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session