"""
Library for interacting with the SQL database.
Inlucedes bells and whistles like connection pooling and logging.

1- Allow Developers manage multiple RDBMS connections with variety of DB
   Engine support such as MSSQL, MYSQL, PostgreSQL,etc

2- Allow Developers manage multiple tenants design in RDBMS

3- Allow Code First auto-generation of database do not care about manual create database at RDMS level.

4- Auto synchronize all columns and tables with the code model even if the database is already created.

5- aUto synchronize all relationships between tables and columns even if the relationships is already created.

6- Allow Synchronization of Indexes and Constraints between code model and database even if the indexes and constraints is already created

Heed: This library is not a replacement for ORM libraries like SQLAlchemy, Django ORM, etc. It is a simple wrapper around the basic SQL commands to make it easier to interact with the database.
It is designed to be used by developers who are not familiar with SQL and want to focus on writing code.
The crucial technique used in this library is wrapper sessionmaker of SQLAlchemy.


"""

import logging
import traceback
from sqlalchemy import create_engine, event, Executable
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text

from sqldb.__utils_my_sql__ import __synchronize_session_with_code_model_mysql__
from sqldb.__utils_sql_server__ import __synchronize_session_with_code_model_sqlserver__
from sqldb.__info__ import IndexInfo
__cache_db_name_and_table_name__ = dict()





def __synchronize_session_with_code_model__(session_instance, entity):
    """
    This method is very special
    Heed: It will synchronize all infor in entity with table in database
    1- Create columns if not exist in table (The purpose of thi lib is to auto-generate tables from code model
     without do migrate db manually).
     2- Create relationships if not exist in table.
     3- Create indexes and constraints if not exist in table.
     4- Create check constraints if not exist in table.
    :param session_instance:
    :param entity:
    :return:
    """
    # use session to create table if not exist in database
    db_name = session_instance.bind.db_name
    dialectical = session_instance.bind.dialect.name
    table_name = entity.__tablename__
    if __cache_db_name_and_table_name__.get(db_name) is None:
        __cache_db_name_and_table_name__[db_name] = dict()
    if __cache_db_name_and_table_name__[db_name].get(table_name) is not None:
        return

    entity.__table__.create(session_instance.bind, checkfirst=True)
    if dialectical == "mysql":
        __synchronize_session_with_code_model_mysql__(session_instance, entity, table_name,db_name)
    if dialectical =="mssql":
        __synchronize_session_with_code_model_sqlserver__(session_instance, entity, table_name, db_name)
    # get all column names of table in database by executing a query


    # update cache
    __cache_db_name_and_table_name__[db_name][table_name] = True

    # create columns if not exist in table


class SQLDB:
    """
    Singleton class for managing SQL database connections and sessions.
    """
    __db_url_cache_instance = dict()

    def __new__(cls, db_url):
        if SQLDB.__db_url_cache_instance.get(db_url) is None:
            SQLDB.__db_url_cache_instance[db_url] = super(SQLDB, cls).__new__(cls)
        return SQLDB.__db_url_cache_instance[db_url]

    def __init__(self, db_url):
        self.db_url = db_url
        self.db_url_no_database = db_url
        self.engine = create_engine(db_url)
        self.dialectical = self.engine.dialect.name
        if self.dialectical == "mssql":
            self.db_url_no_database = '/'.join(self.db_url.split('/')[:-1])

        self.session_factory = sessionmaker(bind=self.engine)
        self.master_session = sessionmaker(bind=self.engine)

        self.db_engine_cache = dict()
        self.session_cache = dict()

        self.__apply_session__(self.session_factory)

    def get_session(self, db_name: str):
        """
        This method is used to get a session for a specific database.
        Heed: This method will create a new database in the database if it does not exist.
        :param db_name:
        :return:
        """

        if self.session_cache.get(db_name) is not None:
            return self.session_cache[db_name]()
        # create database if not exist

        if self.dialectical == "mysql":
            sql_create_db_statement = text(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            with self.master_session() as session:
                session.execute(sql_create_db_statement)
                session.commit()

        elif self.dialectical == "postgresql":
            raise NotImplementedError("PostgreSQL is not supported yet.")
        elif self.dialectical == "mssql":
            conn = self.engine.connect()
            try:
                conn.exec_driver_sql(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{db_name}') CREATE DATABASE {db_name}")
            finally:
                conn.close()

        else:
            raise NotImplementedError(f"{self.dialectical} is not supported yet.")
        # create engine for the specific database
        engine = self.__create_db_engine(db_name)
        # create session for the specific database
        session = sessionmaker(bind=engine)
        setattr(session, 'db_name', db_name)
        self.session_cache[db_name] = session
        self.__apply_session__(session)
        return session()


    def __apply_session__(self, session_factory):
        """
        This method is used to wrap the session_factory with a custom session class.
        it will modify the behavior of the session_factory to return a custom session class.
        such as: query, add, mearge, ...
        :param session_factory:
        :return:
        """

        # check if session_factory is already wrapped with custom session class
        if hasattr(session_factory, '_custom_session_class'):
            return session_factory
        # declare list of methods that can change values of rows of tables in database

        interact_data_methods = ['query', 'add', 'merge', 'delete']

        modify_class = session_factory.class_
        for method_name in interact_data_methods:
            oringal_method = getattr(modify_class, method_name)
            wrapper_method = self.__create_wrapper_method__(oringal_method, method_name)

            setattr(modify_class, method_name, wrapper_method)
        session_factory._custom_session_class = True
        return session_factory


    def __create_db_engine(self, db_name):
        """
        Create engine for a specific database.
        :param db_name:
        :return:
        """
        # check if engine for the specific database is already created
        if self.db_engine_cache.get(db_name) is not None:
            return self.db_engine_cache[db_name]
        # create engine for the specific database

        engine = create_engine(self.db_url_no_database + f"/{db_name}")
        self.db_engine_cache[db_name] = engine
        setattr(engine, 'db_name', db_name)
        return engine

    def __create_wrapper_method__(self, oringal_method, method_name):
        def return_wrapper_method(*args, **kwargs):
            session_instance = args[0]
            setattr(session_instance, f"original_{method_name}", oringal_method)
            entity = args[1]
            # call synchronize_session_with_code_model before executing the method
            __synchronize_session_with_code_model__(session_instance, entity)
            return oringal_method(*args, **kwargs)

        return return_wrapper_method
