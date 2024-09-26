from sqlalchemy import Column, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta
from sqlalchemy.dialects import sqlite

BigIntegerType = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')

def now():
    return datetime.now()+timedelta(hours=8)

class User(Base):
    __tablename__ = "users"
    id = Column(BigIntegerType, primary_key=True, index=True)
    name = Column(String(length=100), index=True, nullable=False)
    role = Column(String(length=20), nullable=False, default="user")
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    is_2fa_enabled = Column(Boolean, default=False, nullable=False)
    otp_secret = Column(String(length=100), nullable=True)
    user_authentication = relationship("UserAuthentication", back_populates="user", uselist=False)
    posts = relationship("Post", back_populates="user")

# from .user_authentication import UserAuthentication
# UserAuthentication.user = relationship(User, primaryjoin=User.id == UserAuthentication.user_id)