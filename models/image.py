from sqlalchemy import Column, String, BigInteger,LargeBinary
from database import Base
from sqlalchemy.dialects import sqlites

BigIntegerType = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')

class Image(Base):
    __tablename__ = "images"
    id = Column(BigIntegerType, primary_key=True, index=True)
    image_path = Column(String(255), nullable=False) 