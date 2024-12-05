from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta
from sqlalchemy.dialects import sqlite

BigIntegerType = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')

def now():
    return datetime.now()+timedelta(hours=8)

class UserAuthentication(Base):
    __tablename__ = "user_authentications"
    id = Column(BigIntegerType, primary_key=True, index=True)
    user_id = Column(BigIntegerType, ForeignKey("users.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    provider = Column(String(length = 100), index=True, nullable=False)
    provider_user_id = Column(String(length = 255), index=True, nullable=False)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    login_fail_time = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="user_authentication", uselist=False)