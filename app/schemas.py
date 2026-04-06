from pydantic import BaseModel,EmailStr,Field,field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

class UserRole(str,Enum):
    admin="admin"
    viewer="viewer"
    analyst="analyst"

class RecordType(str,Enum):
    income="income"
    expense="expense"

class LoginRequest(BaseModel):
    email:EmailStr
    password:str
    
class LoginResponse(BaseModel):
    message:str
    role:UserRole
    user_id:UUID


class UserStatusUpdate(BaseModel):
    is_active:bool

class UserCreate(BaseModel):
    name:str=Field(...,min_length=3,max_length=50)
    email:EmailStr
    password:str=Field(...,min_length=6,max_length=50)
    role:UserRole

class UserResponse(BaseModel):
    id:UUID
    name:str
    email:EmailStr
    role:UserRole
    is_active:bool
    created_at:datetime

    class Config:
        from_attributes=True

class RecordCreate(BaseModel):
    title:str
    amount:float
    type:RecordType
    category:str
    description:Optional[str]=None
    date:datetime
    created_by:UUID
class RecordUpdate(BaseModel):
    title:Optional[str]=None
    amount:Optional[float]=None
    type:Optional[RecordType]=None
    category:Optional[str]=None
    description:Optional[str]=None
    date:Optional[datetime]=None

class RecordResponse(BaseModel):
    id:UUID
    title:str
    amount:float
    type:RecordType
    category:str
    description:Optional[str]=None
    date:datetime
    created_at:datetime
    created_by:UUID

    class Config:
        from_attributes=True