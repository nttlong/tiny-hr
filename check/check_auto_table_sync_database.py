"""
This script is used to check if the auto table sync database is working correctly.
by using package app.db_session.
"""

#  create engine and session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.users import Users
from app.models.roles import Roles

from db_manager.manager import use_db
# create engine and session connect to mysql database
engine = create_engine('mysql+pymysql://root:123456@localhost')
Session = sessionmaker(bind=engine)
session = Session()
use_db(session,"test_db_hrm")
session.query(Users).all()

# create a new user
role = Roles(code="admin", name="admin")
role.Name = "admin"
role.Description = "This is a test role"
session.add(role)
session.commit()

# check if the user is created in the database

