"""
This is the test
use sqldb package connect to MSSQL server
"""
from sqlalchemy import create_engine

from sqldb.db import SQLDB
from app.models.roles import Roles
from sqlalchemy.sql import text
sqldb=SQLDB('mssql+pymssql://sa:123456@localhost/master')


session=sqldb.get_session("hr")
items=session.query(Roles).all()
print(items)