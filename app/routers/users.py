from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.db import Base,engine,get_db
from app.models import User,Records
from app.schemas import UserCreate,UserResponse,UserRole
from app.dependencies import admin_only

router=APIRouter(prefix="/users" ,tags=["Users"])

@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db),role:UserRole=Depends(admin_only)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    new_user=User(name=user.name,email=user.email,password_hash=user.password,role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.get("/",response_model=list[UserResponse])
def get_users(db:Session=Depends(get_db),role:UserRole=Depends(admin_only)):
    users=db.query(User).all()
    return users

