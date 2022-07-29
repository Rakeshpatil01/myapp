
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    # id = Column(String(128), primary_key=True,default=str(uuid.uuid4()))
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True)
    password = Column(String(128))
    username= Column(String(64))
    is_active = Column(String(64), default="True")