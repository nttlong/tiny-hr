"""
Create a MySQL database and table with sample data. code first with SQAlchemy ORM.
Auto create database and table if not exists.
"""
from icecream import ic


from app.utils.security import hash_password,verify_password

pwd="123456abcdef"
hashed_pwd = hash_password(pwd)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import text
# create database if not exists
engine = create_engine('mysql+pymysql://root:123456@localhost', echo=True)

# create base class


# create table class
# from app.models.users import User
from app.models.roles import Role
# from app.models.departments import Department
# from app.models.personal_info import PersonalInfo
# from app.utils.databases import (
#     create_database,
#     switch_database,
#     create_table_if_not_exist,
# )
#
#
#
# # create database if not exists
# # create session
# Session = sessionmaker(bind=engine)
# session = Session()
#
# create_database(session, 'test')
# create_table_if_not_exist(session, Role, 'test')
role1 = Role(
    code='admin',
    name='Admin'
)
# create_table_if_not_exist(session, User, 'test')
# create_table_if_not_exist(session, Department, 'test')
# create_table_if_not_exist(session, PersonalInfo, 'test')
# create_table_if_not_exist(session, Employee, 'test')
# # create sample data
# role1 = Role(
#     code='admin',
#     name='Admin'
# )
#
# user1 = User(Username  ='admin',
#              Email     = 'admin@localhost',
#              Password  = "admin",
#              RoleId    = role1.Id)
# department1 = Department(
#     Name='Test',
#     Code='IT'
# )
# list_of_user =session.query(User).all()
# role = session.query(Role).first()
# role.Users.append(user1)
#
# ic(list_of_user)
# for user in list_of_user:
#     ic(user.__dict__)

