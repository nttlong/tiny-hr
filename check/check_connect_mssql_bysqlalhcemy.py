"""
This code check connection to MSSQL using SQLAlchemy
Driver is : pymssql
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os
# declare connection string
#Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True;
#conn_str = "mssql+pymssql://localhost\SQLEXPRESS:master@localhost:1433/master"
#checkc pymssql connection to sql server
import pymssql
conn = pymssql.connect(
        server=r'localhost',
        user='sa',
        password='123456',
        database='master',
        tds_version='7.3',
        as_dict=True,
    autocommit=True
    )
cur = conn.cursor()
cur.execute(
    "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'hr') CREATE DATABASE hr"
)


# connection string using SQLAlchemy
conn_str = URL.create(
    drivername='mssql+pymssql',
    username='sa',
    password='123456',
    host='localhost',
    port=1433,
    database='master'
)
# create engine
cnn_str = "mssql+pymssql://sa:123456@localhost:1433/master"
conn = pymssql.connect(cnn_str)
engine = create_engine(conn_str)
# check connection
try:
    conn = engine.connect()
    print("Connection successful")
except:
    print("Connection failed")