from tenant_manager.manager import Manager
from sqlalchemy import create_engine
from sqldb.db import SQLDB
# create engi
# Create a connection to the MS SQL Server database use pymssql
cnn_str = "mssql+pymssql://sa:123456@localhost/master"

db=SQLDB(cnn_str)



from app.models.roles import Roles
# create a manager object with mysql





if __name__ == '__main__':
    role = Roles(code="abc", name="Admin")

    db.get_session("hr01").add(role)
    db.get_session("hr01").commit()

    db.get_session("hr01").close()


    print("done")







