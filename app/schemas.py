from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:str

class UserResponse(BaseModel):
    id:UUID
    name:str
    email:EmailStr
    role:str
    is_active:bool
    created_at:datetime

    class Config:
        from_attributes=True

class RecordCreate(BaseModel):
    title:str
    amount:float
    type:str
    category:str
    description:Optional[str]=None
    date:datetime
    created_by:UUID
class RecordUpdate(BaseModel):
    title:Optional[str]=None
    amount:Optional[float]=None
    type:Optional[str]=None
    category:Optional[str]=None
    description:Optional[str]=None
    date:Optional[datetime]=None

class RecordResponse(BaseModel):
    id:UUID
    title:str
    amount:float
    type:str
    category:str
    description:Optional[str]=None
    date:datetime
    created_at:datetime
    created_by:UUID

    class Config:
        from_attributes=True