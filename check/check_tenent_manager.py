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
    db.get_session("hr").query(Roles).filter_by(Code="admin").delete()
    db.get_session("hr").commit()
    db.get_session("hr").close()


    print("done")







