
"""
This is the base model for all the models in the application.
"""

from sqlalchemy import Column, String, DateTime


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
import datetime
import uuid
Base = declarative_base()
class StemModel(Base):
    __abstract__ = True
    Id = Column(String(36),
                primary_key=True,
                unique=True)
class BaseModel(StemModel):
    __abstract__ = True
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    CreatedAt = Column(DateTime, nullable=False,default=datetime.datetime.now(datetime.UTC))
    UpdatedAt = Column(DateTime, nullable=False,default=datetime.datetime.now(datetime.UTC))
    Description = Column(String(255), nullable=True)
    def __init__(self):
        # self.Id = str(uuid.uuid4())
        self.CreatedAt = datetime.datetime.now(datetime.UTC)
        self.UpdatedAt = datetime.datetime.now(datetime.UTC)

class BaseModeCodeName(BaseModel):
    __abstract__ = True
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}
    Code = Column(String(50), unique=True, nullable=False, index=True)
    Name = Column(String(255), index=True, nullable=False)
    def __init__(self, code, name):
        super().__init__()
        self.Code = code
        self.Name = name
        self.Id = str(uuid.uuid4())


