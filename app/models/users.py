
import uuid
from sqlalchemy import Index, create_engine, Column, Integer, String,  DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

from  .base_model import BaseModel   # Define the base class for our models
import uuid
from .roles import Role
import bcrypt
class User(BaseModel):
    __tablename__ = 'Users'
    Username = Column(String(50), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    HashPassword = Column(String(60), nullable=False)
    Salt = Column(String(60), nullable=False)

    RoleId = Column(String(36), ForeignKey(Role.Id), nullable=False)
    Role = relationship(Role)
    def __init__(self, Username, Email, Password, RoleId):

        super().__init__()
        self.Username = Username
        self.Email = Email
        self.RoleId = RoleId
        self.HashPassword, self.Salt = self.hash_password(Password)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # encode the password to bytes before hashing
        return hashed_password.decode('utf-8'), salt.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.HashPassword.encode('utf-8'))   # encode the password to bytes before checking

