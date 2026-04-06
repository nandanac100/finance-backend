from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User,Records
from app.schemas import LoginResponse,LoginRequest
from app.dependencies import admin_only,record_view_role
from uuid import UUID
from passlib.context import CryptContext


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


router=APIRouter(prefix="/auth" ,tags=["Authentication"])


@router.post("/login",response_model=LoginResponse)
def login(user_data:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_data.email).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if not user.is_active:
        raise HTTPException(status_code=403,detail="inactive account")
    verify_password=pwd_context.verify(
        user_data.password,user.password_hash
    )
    if not verify_password:
        raise HTTPException(status_code=401,detail="Invalid password")
    
    return {
        "message":"Login successful",
        "role":user.role,
        "user_id":user.id
    }

