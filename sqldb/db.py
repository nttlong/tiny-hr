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
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text

__cache_db_name_and_table_name__ = dict()
__cache_db_index__ = dict()
__cache_model_index__ = dict()
class IndexInfo:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns


def __get_all_indexes_in_database__(session_instance, table_name)->list[IndexInfo]:
    """
    This method is used to get all indexes in a table in a database.
    :param session_instance:
    :param table_name:
    :return:
    """
    if __cache_db_index__.get(table_name) is not None:
        return __cache_db_index__[table_name]

    sql_get_indexes = text(f"SELECT INDEX_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{session_instance.bind.db_name}'")
    indexes = session_instance.execute(sql_get_indexes).fetchall()
    index_info_list = []
    for index in indexes:
        index_info = IndexInfo(index[0], [index[1]])
        index_info_list.append(index_info)
    # cache
    __cache_db_index__[table_name] = index_info_list
    return index_info_list


def __get_all_indexes_in_code_model__(entity)->list[IndexInfo]:
    """
    This method is used to get all indexes in a table in a database.
    :param session_instance:
    :param table_name:
    :return:
    """
    if __cache_model_index__.get(entity.__table__.name) is not None:
        return __cache_model_index__[entity.__tablename__.name]
    if entity.__table__.indexes is None:
        return []
    index_info_list = []
    for index in entity.__table__.indexes:
        index_info = IndexInfo(index.name, [column.name for column in index.columns])
        index_info_list.append(index_info)
    # cache
    __cache_model_index__[entity.__table__.name] = index_info_list
    return index_info_list


def __synchronize_all_indexes__(session_instance, entity,table_name):
    """
    This method is used to synchronize all indexes  between code model and database.
    :param session_instance:
    :param entity:
    :param table_name:
    :return:
    """
    db_index: list[IndexInfo] = __get_all_indexes_in_database__(session_instance, table_name)
    model_index: list[IndexInfo] = __get_all_indexes_in_code_model__(entity)



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
    table_name = entity.__tablename__
    if __cache_db_name_and_table_name__.get(db_name) is None:
        __cache_db_name_and_table_name__[db_name] = dict()
    if __cache_db_name_and_table_name__[db_name].get(table_name) is not None:
        return

    entity.__table__.create(session_instance.bind, checkfirst=True)
    # get all column names of table in database by executing a query
    sql_get_column_names = text(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{db_name}'")
    column_names_in_db = [row[0] for row in session_instance.execute(sql_get_column_names).fetchall()]
    # get all column names of table in code model
    column_names_in_code_model = [column.name for column in entity.__table__.columns]
    sync_cols = list(set(column_names_in_code_model) - set(column_names_in_db))
    for col in sync_cols:
        # create column in database
        col_type = entity.__table__.columns[col].type.compile(dialect=session_instance.bind.dialect)

        sql_create_column = text(f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}")
        session_instance.execute(sql_create_column)
        # get defult value of column in code model
        default_value = entity.__table__.columns[col].default
        if default_value is not None:
            sql_set_default_value = text(f"ALTER TABLE {table_name} ALTER COLUMN {col} SET DEFAULT {default_value.arg}")
            session_instance.execute(sql_set_default_value)
    __synchronize_all_indexes__(session_instance, entity,table_name)

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
        self.engine = create_engine(db_url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.master_session = sessionmaker(bind=self.engine)

        self.db_engine_cache = dict()
        self.session_cache= dict()

        self.__apply_session__(self.session_factory)

    def get_session(self,db_name:str):
        """
        This method is used to get a session for a specific database.
        Heed: This method will create a new database in the database if it does not exist.
        :param db_name:
        :return:
        """

        if self.session_cache.get(db_name) is not None:
            return self.session_cache[db_name]()
        # create database if not exist
        sql_create_db_statement = text( f"CREATE DATABASE IF NOT EXISTS {db_name};")
        with self.master_session() as session:
            session.execute(sql_create_db_statement)
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

        #check if session_factory is already wrapped with custom session class
        if hasattr(session_factory, '_custom_session_class'):
            return session_factory
        # declare list of methods that can change values of rows of tables in database

        interact_data_methods = ['query', 'add','merge', 'delete']

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
        engine = create_engine(self.db_url+f"/{db_name}")
        self.db_engine_cache[db_name] = engine
        setattr(engine, 'db_name', db_name)
        return engine

    def __create_wrapper_method__(self, oringal_method, method_name):
        def return_wrapper_method(*args, **kwargs):

            session_instance = args[0]
            setattr(session_instance,f"original_{method_name}",oringal_method)
            entity = args[1]
            # call synchronize_session_with_code_model before executing the method
            __synchronize_session_with_code_model__(session_instance, entity)
            return oringal_method(*args, **kwargs)
        return return_wrapper_method














