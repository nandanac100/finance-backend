from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.db import Base,engine,get_db
from app.models import User,Records
from app.schemas import UserCreate,UserResponse,UserRole,UserStatusUpdate,RecordResponse
from app.dependencies import admin_only,record_view_role
from uuid import UUID


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
def get_users(db:Session=Depends(get_db),role:UserRole=Depends(record_view_role)):
    users=db.query(User).all()
    return users

@router.get("/{user_id}",response_model=list[RecordResponse])
def get_user_records(user_id:UUID,db:Session=Depends(get_db)):
    records=db.query(Records).filter(Records.created_by==user_id).all()
    if not records:
        raise HTTPException(status_code=404,detail="record not found")
    return records

@router.patch("/{user_id}/status",response_model=UserResponse)
def create_user(user_id:UUID,status_data:bool,db:Session=Depends(get_db),role:UserRole=Depends(admin_only)):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,details="user not found")
    user.is_active=status_data
    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_product(user_id:UUID,db:Session=Depends(get_db),role:UserRole=Depends(admin_only)):
    user=db.query(User).filter(User.id==user_id).first()
    if user:
       db.delete(user)
       db.commit() 
    else: 
        return "no user found"