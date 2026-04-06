from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db import Base,engine,get_db
from app.models import User,Records
from app.schemas import UserCreate,UserResponse

Base.metadata.create_all(bind=engine)
app=FastAPI()

@app.get("/")
def home():
    return "hello world"

@app.post("/user",response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    new_user=User(name=user.name,email=user.email,password_hash=user.password,role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@app.get("/user",response_model=list[UserResponse])
def get_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users