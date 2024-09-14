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
        self.db_engines = {}
        self.tenants = {}
        self.db_cache = {}




    def __sync_table_to_database__(self,session:Session,entity,db_name:str):
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
        if __table_sync_cache__.get(db_name,{}).get(entity.__tablename__):
            return
        entity.__table__.create(session.bind, checkfirst=True)
        for column in entity.__table__.columns:
            # check if column name is not in table
            if not session.execute(text(f"SHOW COLUMNS FROM {entity.__tablename__} LIKE '{column.name}'")).first():
                # add column to table
                # get db column _type of column in entity by using sqlalchemy.types
                db_column_type = column._type.compile(self.engine.dialect)

                session.execute(text(f"ALTER TABLE {entity.__tablename__} ADD COLUMN {column.name} {db_column_type};"))
        # add table to cache
        __table_sync_cache__.setdefault(db_name,{})[entity.__tablename__] = True

    def __apply_auto_create_table__(self, session:Session,db_name:str)->Session:
        """
        Apply auto create table feature to the given session.


        """
        old_query = session.query
        def query(entity):
            # get tabe name of entity
            table_name = entity.__tablename__
            db = self.db_cache.get(db_name)
            if isinstance(db,dict) and db.get(table_name) is not None:
                return old_query(entity)
            # check if table is already exist in database
            self.__sync_table_to_database__(session, entity, db_name)
            # mark table is ready created in db_cache
            self.db_cache.setdefault(db_name,{})[table_name] = True

            return old_query(entity)
        session.query = query
        old_add = session.add
        def add(entity):
            if entity is None:
                return
            # get tabe name of entity
            table_name = entity.__tablename__
            db = self.db_cache.get(db_name)
            if isinstance(db,dict) and db.get(table_name) is not None:
                return old_add(entity)
            # check if table is already exist in database
            self.__sync_table_to_database__(session, entity, db_name)
            # mark table is ready created in db_cache
            self.db_cache.setdefault(db_name,{})[table_name] = True

            return old_add(entity)
        session.add = add
        old_merge = session.merge
        def merge(entity):
            # get tabe name of entity
            if entity is None:
                return
            # get tabe name of entity
            table_name = entity.__tablename__
            db = self.db_cache.get(db_name)


            if isinstance(db,dict) and db.get(table_name) is not None:
                return old_merge(entity)
            # check if table is already exist in database
            self.__sync_table_to_database__(session, entity, db_name)
            return old_merge(entity)
        session.merge = merge
        old_delete = session.delete
        def delete(entity):
            if entity is None:
                return
            # get tabe name of entity
            table_name = entity.__tablename__
            db = self.db_cache.get(db_name)

            if isinstance(db,dict) and db.get(table_name) is not None:
                return old_delete(entity)
            # check if table is already exist in database
            self.__sync_table_to_database__(session, entity, db_name)
            return old_delete(entity)
        session.delete = delete
        return session
    def db_session(self, db_name: str)->Session:

        #check if db_name in session_cache
        if self.db_cache.get(db_name) is None:
            sql = f"CREATE DATABASE IF NOT EXISTS {db_name};"
            sql_stmt = text(sql)
            with self.engine.connect() as conn:
                conn.execute(sql_stmt)

        # create new session
        if self.db_engines.get(db_name) is None:
            self.db_engines[db_name] = create_engine(self.db_url + "/" + db_name)

        session = sessionmaker(bind=self.db_engines[db_name] )()
        session.execute(text(f"USE {db_name};"))
        if self.db_cache.get(db_name) is None:
            self.db_cache[db_name] = dict()

        session = self.__apply_auto_create_table__(session,db_name)
        return session
