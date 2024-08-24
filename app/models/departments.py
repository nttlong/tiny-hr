
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import GUID
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Department(Base):
    """
    The info of department

    """
    __tablename__ = 'departments'

    Id = Column(GUID, primary_key=True)
    Name = Column(String(100), nullable=False)
    Code = Column(String(10), nullable=False)
    ParentId = Column(GUID, ForeignKey('departments.Id'))
    Description = Column(String(500), nullable=True)

    employees = relationship('Employee', back_populates='department',lazy="joined")

