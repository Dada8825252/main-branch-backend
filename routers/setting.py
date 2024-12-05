from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from schemas.user import UserProfile, UserSettings
from controllers.auth import get_current_user
from controllers import setting
from database import get_db
from schemas.user import UserRead

setting_router = APIRouter()

@setting_router.get('/', response_model=UserProfile)
async def get_user_data(db: Session = Depends(get_db), user: UserProfile = Depends(get_current_user)):
    return setting.get_user_data(db=db, user=user)

@setting_router.put('/username')
async def update_user_name(user_item: UserSettings, db: Session = Depends(get_db), user: UserProfile = Depends(get_current_user)):
    return setting.update_user_name(user_item=user_item, db=db, user=user)

@setting_router.put('/otp')
async def update_user_otp(user_item: UserSettings, db: Session = Depends(get_db), user: UserProfile = Depends(get_current_user)):
    return setting.update_user_otp(user_item=user_item, db=db, user=user)