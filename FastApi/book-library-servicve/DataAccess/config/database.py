from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Database_Url = (
    "mssql+pyodbc://@(localdb)\MSSQLLocalDB/LibraryDatabase"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(Database_Url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get DB session per request
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()