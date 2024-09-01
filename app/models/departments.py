
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from .base_model import BaseModeCodeName
class Departments(BaseModeCodeName):
    """
    The info of department

    """
    __tablename__ = 'Departments'


    ParentId = Column(String(32), ForeignKey('Departments.Id'))
    # parent = relationship('Department', remote_side=[BaseModeCodeName.Id])

    # users = relationship("User", back_populates="Roles")
    employees = relationship('Employees', back_populates='department')

