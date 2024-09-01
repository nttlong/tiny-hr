"""
All models are imported here.
"""
from .roles import Roles
from .users import Users
from .departments import Departments
from .employees import Employees
from .personal_info import PersonalInfo
from sqlalchemy.engine import Engine
__models__ = [Roles, Users, Departments, Employees, PersonalInfo]
def startup_with_db(engine: Engine,db_name:str):
    """
    This function starts the database with the given engine and database name.
    It will check all change in __models__ and create the tables if they don't exist.
    It also creates new column from model if that column doesn't exist.
    :param engine:
    :param db_name:
    :return:
    """
    #create session from en
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    #create tables if they don't exist
    for model in __models__:
