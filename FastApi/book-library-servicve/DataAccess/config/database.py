from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import get_connection_settings

settings = get_connection_settings()

engine = create_engine(str(settings.DatabaseUrl), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get DB session per request
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()