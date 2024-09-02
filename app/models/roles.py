"""
This file contains the Roles model using sqlalchemy declarative .
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

import uuid
from .base_model import  BaseModel,BaseModeCodeName,Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean
class Roles(BaseModeCodeName):

    __tablename__ = "Roles"
    IsAdmin = Column(Boolean, default=False)
    IsSuperAdmin = Column(Boolean, default=False)
    #users = relationship("Users", back_populates="role")
    # view = Column(String(255), nullable=True)


