from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db import Base,engine,get_db
from app.models import User,Records
from app.schemas import UserCreate,UserResponse
from app.routers import users,records,dashboard,auth

Base.metadata.create_all(bind=engine)
app=FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return "hello world"
