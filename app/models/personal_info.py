"""
This file contains the PersonalContact inhertance StemModel class.
"""
from .base_model import StemModel
from sqlalchemy import Column, String

class PersonalInfo(StemModel):
    """
    The info of personal contact

    """
    __tablename__ = 'personal_info'
    FirstName = Column(String(100), nullable=False,index=True)
    LastName = Column(String(100), nullable=False,index=True)
    Email = Column(String(100), nullable=False, unique=True,index=True)
    Phone = Column(String(20), nullable=False,index=True)
    Address = Column(String(200), nullable=False,index=True)
    City = Column(String(100), nullable=False,index=True)
    State = Column(String(100), nullable=False,index=True)
    ZipCode = Column(String(20), nullable=False,index=True)
    IdCard = Column(String(20), nullable=False,index=True)
    BirthDate = Column(String(10), nullable=False,index=True)
    Gender = Column(String(10), nullable=False,index=True)
    MaritalStatus = Column(String(100), nullable=False,index=True)
