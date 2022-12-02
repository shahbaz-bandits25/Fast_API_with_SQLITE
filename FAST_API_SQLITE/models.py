from sqlalchemy import  Column,Integer, String
from db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)