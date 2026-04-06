from fastapi import FastAPI
from app.db import Base,engine
from app.models import User,Records

Base.metadata.create_all(bind=engine)
app=FastAPI()

@app.get("/")
def home():
    return "hello world"