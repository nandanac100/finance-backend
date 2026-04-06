from fastapi import FastAPI,Depends,HTTPException,APIRouter
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User,Records
from app.schemas import RecordCreate,RecordResponse,RecordUpdate,UserRole
from uuid import UUID
from sqlalchemy import func
from app.dependencies import record_view_role


router=APIRouter(prefix="/dashboard" ,tags=["Daashboard"])

@router.get("/summary")
def get_summary(db:Session=Depends(get_db),role:UserRole=Depends(record_view_role)):
    net_income=db.query(func.sum(Records.amount)).filter(Records.type=="income").scalar() or 0
    net_expense=db.query(func.sum(Records.amount)).filter(Records.type=="expense").scalar() or 0
    net_balance=net_income-net_expense
    return {
        "total_income":net_income,
        "total_expense":net_expense,
        "net_balance":net_balance
    }

@router.get("/category-totals")
def get_catetegory_totals(db:Session=Depends(get_db),role:UserRole=Depends(record_view_role)):
    category_totals=(db.query(Records.category,func.sum(Records.amount).label("total")).group_by(Records.category).all())
    return [
        {
            "category":category,
            "total":total
        }for category,total in category_totals
    ]

@router.get("/recent-activities")
def get_recent_activities(db:Session=Depends(get_db)):
    records=(
        db.query(Records).order_by(Records.created_at.desc()).limit(5).all()
        )
    return records

@router.get("/monthly-trends")
def get_monthly_trends(db:Session=Depends(get_db),role:UserRole=Depends(record_view_role)):
    monthly_trends=(
        db.query(func.date_trunc("month",Records.date).label("month"),Records.type,func.sum(Records.amount).label("total")).group_by(func.date_trunc("month",Records.date),Records.type).order_by(func.date_trunc("month",Records.date)).all()
    )

    return [
        {
            "month": month.strftime("%Y-%m"),
            "type": record_type,
            "total":total
        }for month,record_type,total in monthly_trends
    ]