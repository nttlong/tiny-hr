"""
This file contains the Roles model using sqlalchemy declarative .
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

import uuid
from .base_model import  BaseModel,BaseModeCodeName,Base

class Roles(BaseModeCodeName):

    __tablename__ = "Roles"
    # users = relationship("Users", back_populates="role")
    # view = Column(String(255), nullable=True)


