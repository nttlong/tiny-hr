import typing
import uuid

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the base class for our models
Base = declarative_base()

# Define the Employee model
from .base_model import  BaseModeCodeName

from .departments import Departments
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey

class Employees(BaseModeCodeName):
    """
    The info of employee

    """
    __tablename__ = 'Employees'



    JobTitle = Column(String(100), nullable=False)
    
    DepartmentId = Column(String(32), ForeignKey(Departments.Id), nullable=False)
    department = relationship(Departments)


    Salary = Column(Integer, nullable=False)
    IsActive = Column(Boolean, nullable=False)

    HireDate = Column(DateTime, nullable=False)

