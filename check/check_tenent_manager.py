from tenant_manager.manager import Manager
from sqlalchemy import create_engine
# create engi
engine = create_engine('mysql+pymysql://root:123456@localhost')


from app.models.roles import Roles
# create a manager object with mysql



manager = Manager('mysql+pymysql://root:123456@localhost')
manager2=Manager('mysql+pymysql://root:123456@localhost')
test_tenant = manager["db_test"]
hr_tenant = manager["db_hr"]
test_tenant.query(test_tenant.session(),Roles).first()
print(manager2==manager)



