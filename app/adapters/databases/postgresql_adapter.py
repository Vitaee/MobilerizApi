from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


class PostgreSQLAdapter:
    def __init__(self):
        self.engine = create_engine(settings.POSTGRESQL_DATABASE_URI)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()