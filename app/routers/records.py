from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User,Records
from app.schemas import RecordCreate,RecordResponse,RecordUpdate
from uuid import UUID

router=APIRouter(prefix="/records" ,tags=["Records"])

@router.post("/",response_model=RecordResponse)
def create_record(record:RecordCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.id==record.created_by).first()
    if not existing_user:
        raise HTTPException(status_code=404,detail="user not found")
    new_record=Records(
        title=record.title,
        amount=record.amount,
        type=record.type,
        category=record.category,
        description=record.description,
        date=record.date,
        created_by=record.created_by
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record) 
    return new_record

@router.get("/",response_model=list[RecordResponse])
def get_records(db:Session=Depends(get_db)):
    records=db.query(Records).all()
    return records
@router.get("/{record_id}",response_model=RecordResponse)
def get_record(record_id:UUID,db:Session=Depends(get_db)):
    record=db.query(Records).filter(Records.id==record_id).first()
    if not record:
        raise HTTPException(status_code=404,detail="record not found")
    return record
@router.put("/{record_id}",response_model=RecordResponse)
def update_record(record_id:UUID,update_data:RecordUpdate,db:Session=Depends(get_db)):
    record=db.query(Records).filter(Records.id==record_id).first()
    if not record:
        raise HTTPException(status_code=404,detail="record not found")
    record.title=update_data.title
    record.amount=update_data.amount
    record.type=update_data.type
    record.category=update_data.category
    record.description=update_data.description
    record.date=update_data.date
    db.commit()
    db.refresh(record) 
    return record

@router.delete("/{record_id}")
def delete_product(record_id:UUID,db:Session=Depends(get_db)):
    record=db.query(Records).filter(Records.id==record_id).first()
    if record:
       db.delete(record)
       db.commit() 
    else: 
        return "no record found"
