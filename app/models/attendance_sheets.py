from sqlalchemy import Column, Integer, Date, Time, Interval, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AttendanceSheets(Base):
    """
    The info of attendance sheets

    """
    __tablename__ = 'attendance_sheets'

    Id = Column(Integer, primary_key=True)
    Date = Column(Date, nullable=False)
    StartTime = Column(Time, nullable=False)
    EndTime = Column(Time, nullable=False)
    Duration = Column(Interval, nullable=False)
    EmployeeId = Column(Integer, ForeignKey('employees.Id'), nullable=False)
    Employee = relationship('Employee', backref='attendance_sheets')
    ProjectId = Column(Integer, ForeignKey('projects.id'), nullable=False)
    Project = relationship('Projects', backref='attendance_sheets')
    Status = Column(String(20), nullable=False)
    Comments = Column(String(255), nullable=True)
    CreatedAt = Column(Date, default=datetime.utcnow)
    UpdatedAt = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)