"""
This script will get all the tables in the database and print them out. by using the following command: Sqlalchemy.
"""

from sqlalchemy import create_engine, MetaData

# create a connection to the database
engine = create_engine('mysql+pymysql://root:123456@localhost/test')
metadata = MetaData()
metadata.reflect(bind=engine)
table_names = metadata.tables.keys()

# print out all the tables in the database
print(table_names)