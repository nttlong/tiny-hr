from tenant_manager.manager import Manager
from sqlalchemy import create_engine
# create engi
engine = create_engine('mysql+pymysql://root:123456@localhost')


from app.models.roles import Roles
# create a manager object with mysql





if __name__ == '__main__':
    manager = Manager('mysql+pymysql://root:123456@localhost')
    session = manager.db_session("hrm")

    role = session.query(Roles).filter_by(Code="admin").first()
    session.delete(role)

    session.commit()
    session.close()

    print("done")







