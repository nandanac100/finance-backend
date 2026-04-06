from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User,Records
from app.schemas import RecordCreate,RecordResponse,RecordUpdate
from uuid import UUID
from sqlalchemy import func

router=APIRouter(prefix="/dashboard" ,tags=["Daashboard"])

@router.get("/summary")
def get_summary(db:Session=Depends(get_db)):
    net_income=db.query(func.sum(Records.amount)).filter(Records.type=="income").scalar() or 0
    net_expense=db.query(func.sum(Records.amount)).filter(Records.type=="expense").scalar() or 0
    net_balance=net_income-net_expense
    return {
        "total_income":net_income,
        "total_expense":net_expense,
        "net_balance":net_balance
    }
