from app.database import Base
from sqlalchemy import String,Integer,Column,Boolean
class User(Base):
    __tablename__="users"
    id=Column(Integer,autoincrement=True,primary_key=True)
    email=Column(String,unique=True,nullable=False,index=True)
    hashed_password=Column(String,nullable=False)
    role=Column(String,default="user")
    is_active=Column(Boolean,default=True)
    is_verified=Column(Boolean,default=False)
    verification_token=Column(String,nullable=True)     