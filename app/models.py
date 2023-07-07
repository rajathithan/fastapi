from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP, text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(type_=Integer,primary_key=True,index=True)
    title = Column(type_=String,nullable=False,index=True)
    content = Column(type_=String, nullable=False)
    published = Column(type_=Boolean,nullable=False, server_default='TRUE')
    created_at = Column(type_=TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    
    
class User(Base):
    __tablename__ = 'Users'
    id = Column(type_=Integer,primary_key=True,index=True)
    email = Column(type_=String,nullable=False,unique=True)
    password = Column(type_=String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))