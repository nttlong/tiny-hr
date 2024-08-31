from app.models.roles import Role
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:123456@localhost', echo=True)

# create base class
from app.models.employees import Employee
from app.models.departments import Department

from app.models.roles import Role
registry.configure()
role =Role(
    code='admin',
    name='Admin'
)


print(role.code)
print(role.name)