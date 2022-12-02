from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemy_Database_URL = "sqlite:///./users.db"

engine = create_engine(SqlAlchemy_Database_URL, connect_args = {"check_same_thread": False})

sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
