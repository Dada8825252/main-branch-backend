from sqlalchemy import Column, String, BigInteger,LargeBinary
from database import Base
from sqlalchemy.dialects import sqlite

BigIntegerType = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')

class Image(Base):
    __tablename__ = "images"
    image_path = Column(String(255), nullable=False, primary_key=True, index=True) 