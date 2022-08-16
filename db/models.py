from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    # user_id=Column(Integer,ForeignKey('users.id'))
    items= relationship("DbArticle", back_populates="user")

class DbArticle(Base):
    __tablename__='articles'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(String)
    published=Column(String)
    user_id=Column(Integer,ForeignKey('users.id'))
    user = relationship("DbUser", back_populates="items")


