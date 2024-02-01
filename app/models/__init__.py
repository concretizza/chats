import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url = 'postgresql://root:4321@localhost/chats'
db_url = os.getenv('DB_URL')
if db_url is not None:
    url = db_url

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
