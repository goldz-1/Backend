from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String, unique=True, index=True)
    fcm_token = Column(String, nullable=True)

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=True)
