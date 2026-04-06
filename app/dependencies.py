from fastapi import Header,HTTPException,Depends
from app.schemas import UserRole

def get_current_role(x_role:UserRole=Header(...)):
    return x_role
"""
def dashboard_view_role(x_role:UserRole=Header(...)):
    return x_role
    
"""
def admin_only(role:UserRole=Depends(get_current_role)):
    if role!=UserRole.admin:
        raise HTTPException(status_code=403,detail="Access only for admin")
    return role
def record_view_role(role:UserRole=Depends(get_current_role)):
    if role not in [UserRole.admin,UserRole.analyst]:
        raise HTTPException(status_code=403,detail="Access only for admin and analyst")
    return role