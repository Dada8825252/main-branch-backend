from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserProfile, UserSettings
from models.user import User
from common.role import *
from controllers.otp import setup_otp

def transfer_profile(db_user: User) -> UserProfile:
    return UserProfile(
        id=db_user.id,
        name=db_user.name,
        role=db_user.role,
        is_2fa_enabled=db_user.is_2fa_enabled,
        otp_secret = db_user.otp_secret,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )

def get_user_data(db: Session, user: UserProfile):
    db_profile = db.query(User).filter(User.id == user.id).first()

    if user.role == ANYMOUS:
        raise HTTPException(
            status_code=401,
            detail="You should login first."
        )
    
    return transfer_profile(db_profile)

def update_user_name(user_item: UserSettings, db: Session, user: UserProfile):
    db_profile = db.query(User).filter(User.id == user.id).first()

    if user.role == ANYMOUS:
        raise HTTPException(
            status_code=401,
            detail="You should login first."
        )
    
    db_profile.name = user_item.name
    db.commit()
    db.refresh(db_profile)

    return transfer_profile(db_profile)

def update_user_otp(user_item: UserSettings, db: Session, user: UserProfile):
    db_profile = db.query(User).filter(User.id == user.id).first()
    
    if user.role == ANYMOUS:
        raise HTTPException(
            status_code=401,
            detail="You should login first."
        )

    if user_item.is_2fa_enabled :
        if not db_profile.is_2fa_enabled:
            db_profile.otp_secret= setup_otp(db_profile.id)

    db_profile.is_2fa_enabled = user_item.is_2fa_enabled
    db.commit()
    db.refresh(db_profile)

    return transfer_profile(db_profile)