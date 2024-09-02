from sqldb.db import SQLDB

# make sure is singleton
# create two SQLDB objects connect to MySQL database
db_a = SQLDB(db_url="mysql+pymysql://root:123456@localhost")
db_b = SQLDB(db_url="mysql+pymysql://root:123456@localhost")

hr_session = db_b.get_session(db_name="hr")
from app.models.roles import Roles


hr_session.commit()

role_list = hr_session.query(Roles).all()
role = hr_session.query(Roles).first()
print(role_list)

# check if they are the same object
print(db_a == db_b)  # True
adm_session = db_a.get_session(db_name="admindb")
print(db_a == db_b)  # False
print(db_a == adm_session.db)  # True
