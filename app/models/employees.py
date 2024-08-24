import typing
import uuid
from sqlalchemy import create_engine, Column, Integer, String, GUID, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the base class for our models
Base = declarative_base()

# Define the Employee model

class Employee(Base):
    """
    The info of employee

    """
    __tablename__ = 'employees'

    Id = Column(GUID, default=lambda: uuid.uuid4(), primary_key=True)
    Code = Column(String(50), nullable=False, unique=True)
    Name = Column(String(100), nullable=False)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    BirthDate = Column(DateTime, nullable=False)
    Gender = Column(String(10), nullable=False)
    JobTitle = Column(String(100), nullable=False)
    
    DepartmentId = Column(GUID, ForeignKey('departments.Id'), nullable=False)

    Salary = Column(Integer, nullable=False)
    IsActive = Column(Boolean, nullable=False)
    Department = Column(String(100), nullable=False)
    HireDate = Column(DateTime, nullable=False)
    MaritalStatus = Column(String(10), nullable=False)
    Email = Column(String(100), nullable=False, unique=True)
    Phone = Column(String(20), nullable=False)
    Address = Column(String(200), nullable=False)
    City = Column(String(100), nullable=False)
    State = Column(String(100), nullable=False)
    ZipCode = Column(String(20), nullable=False)
    Description = Column(String(500), nullable=True)