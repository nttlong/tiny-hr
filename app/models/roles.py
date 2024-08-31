"""
This file contains the Role model using sqlalchemy declarative .
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

import uuid
from .base_model import  BaseModel,BaseModeCodeName,Base

class Role(BaseModeCodeName):

    __tablename__ = "Roles"
    users = relationship("User", back_populates="Role")


