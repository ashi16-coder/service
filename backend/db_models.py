from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String(255), unique=True, nullable=False, index=True)
    password   = Column(String(255), nullable=False)
    mobile     = Column(String(15),  unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
