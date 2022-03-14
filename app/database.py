from re import A
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="testapi",
#             user="postgres",
#             password="09085545655",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Connected to database")
#         break
#     except Exception as error:
#         print("Failed connecting to database")
#         print("Error:", error)
#         time.sleep(3)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
