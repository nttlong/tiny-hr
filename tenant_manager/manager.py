"""
This file is responsible for managing the tenants.
Include class Tenant and Manager

Manager class: responsible for managing the tenants
Tenant class: responsible for managing the tenant details

"""

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text
__table_sync_cache__ = dict()
"""
__table_sync_cache__ is a cache for storing the table schema of the entities.
The key of the cache is db name and the value is a dictionary of table name in that database
ex: __table_sync_cache__ = {"tenant1": {"users": True, "roles": True}
"""
class Tenant:
    def __init__(self, db_url:str, tenant_db_name:str):
        self.tenant_db_name = tenant_db_name
        self.engine = create_engine(db_url+"/"+tenant_db_name)

    def session(self)->Session:
        """
        Create a new session for the given tenant.
        :return:
        """

       # create session

        session = sessionmaker(bind=self.engine)()
        # use the given tenant database

        # use_db_stmt = text(f"USE {self.tenant_db_name};")
        # session.execute(use_db_stmt)
        sql_stmt = text(f"USE {self.tenant_db_name};")
        session.execute(sql_stmt)
        return session
    def query(self,session:Session,entity):
        """
        Create table for the given entity.
        Query the given entity from the given session.
        :param session:
        :param entity:
        :return:
        """

        # create table for the given entity

        # synchronize all columns of table to database
        # check if database name and table is already exist in cache
        if __table_sync_cache__.get(self.tenant_db_name,{}).get(entity.__tablename__):
            return session.query(entity)
        entity.__table__.create(session.bind, checkfirst=True)
        for column in entity.__table__.columns:
            # check if column name is not in table
            if not session.execute(text(f"SHOW COLUMNS FROM {entity.__tablename__} LIKE '{column.name}'")).first():
                # add column to table
                # get db column type of column in entity by using sqlalchemy.types
                db_column_type = column.type.compile(self.engine.dialect)

                session.execute(text(f"ALTER TABLE {entity.__tablename__} ADD COLUMN {column.name} {db_column_type};"))
        # add table to cache
        __table_sync_cache__.setdefault(self.tenant_db_name,{})[entity.__tablename__] = True
        return session.query(entity)





class Manager:
    """
    Singleton class for managing the tenants.
    """

    __db_url_cache_instance = dict()

    def __new__(cls, db_url:str):
        if Manager.__db_url_cache_instance.get(db_url) is None:
            Manager.__db_url_cache_instance[db_url] = super(Manager, cls).__new__(cls)
        return Manager.__db_url_cache_instance[db_url]
    def __init__(self, db_url:str):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.tenants = {}
    def __getitem__(self, item)->Tenant:
        return self.get_tenant(item)
    def get_tenant(self, tenant_db_name: str) -> Tenant:
        """
        Create a new tenant and return the Tenant object.
        """
        # For code first approach, we can create the database if datbase is not exist

        sql = f"CREATE DATABASE IF NOT EXISTS {tenant_db_name};"
        sql_stmt = text(sql)
        with self.engine.connect() as conn:
            conn.execute(sql_stmt)
        if tenant_db_name in self.tenants:
            return self.tenants[tenant_db_name]
        else:
            tenant = Tenant(self.db_url, tenant_db_name)
            self.tenants[tenant_db_name] = tenant
            return tenant