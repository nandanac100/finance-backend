from app.db import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import Column,String,Boolean,DateTime,Float,ForeignKey,Enum
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name=Column(String,nullable=False)
    email=Column(String,nullable=True,unique=True)
    password_hash=Column(String,nullable=False)
    role=Column(Enum("admin","viewer","analyst",name="user_roles"),nullable=False,default="viewer")
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    records=relationship("Records",back_populates="user")




class Records(Base):
    __tablename__="records"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    title=Column(String,nullable=False)
    amount=Column(Float,nullable=False)
    type=Column(Enum("expense","income",name="record_type"),nullable=False)
    category=Column(String,nullable=False)
    description=Column(String,nullable=False)
    date=Column(DateTime,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    created_by=Column(UUID(as_uuid=True),ForeignKey("users.id"))
    user=relationship("User",back_populates="records")

