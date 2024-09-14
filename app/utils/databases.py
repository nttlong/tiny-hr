"""
This file is collecting all the database related functions.
Such as:
- Check if database is exiting by using sqlalchemy
- Create database if not exist
- get all tables in database
- get all columns of a table is database
- get all columns of SqLAlchemy model
- extract all columns of SqLAlchemy model that is not in columns of table in database
- create new columns of SqLAlchemy model in database if not exist in database


"""
import traceback

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine
from sqlalchemy.ext.declarative import declarative_base



def check_database_exist(session: Session, database_name: str) -> bool:
    """
    Check if database is exiting by using sqlalchemy  session
    :_type session: sqlalchemy.orm.session.Session
    :_type database_name: str
    :param session:
    :param database_name:
    :return:
    """
    sql_statement = text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name}'")
    result = session.execute(sql_statement)

    if result.rowcount > 0:
        return True
    else:
        return False


def create_database(session: Session, database_name: str) -> bool:
    """
    Create database if not exist  by using sqlalchemy.orm.session
    :_type session: sqlalchemy.orm.session.Session
    :_type database_name: str
    :param session:
    :param database_name:
    :return: if  exist database return False, else True
    """
    try:
        sqL_statement = text(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        session.execute(sqL_statement)
        return False
    except:
        return True


def switch_database(session: Session, database_name: str) -> Session:
    """
    Switch database by using sqlalchemy.orm.session
    :_type session: sqlalchemy.orm.session.Session
    :_type database_name: str
    :param session:
    :param database_name:
    :return:
    """
    sqL_statement = text(f"USE {database_name}")
    session.execute(sqL_statement)
    return session


def get_all_tables(session: Session, database_name: str) -> list:
    """
    Get all tables in database  by using sqlalchemy.orm.session
    :_type session: sqlalchemy.orm.session.Session
    :_type database_name: str
    :param session:
    :return: list of tables
    """

    sql_statement = text(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{database_name}' "
        f"AND table_type = 'BASE TABLE'")
    result = session.execute(sql_statement)
    tables = [row[0] for row in result]
    return tables


def get_all_columns_of_table(session: Session, database_name: str, table_name: str) -> list:
    """
    Get all columns of a table is database by using sqlalchemy.orm.session
    :_type session: sqlalchemy.orm.session.Session
    :_type database_name: str
    :_type table_name: str
    :param session:
    :param table_name:
    :return:
    """
    sql_statement = text(
        f"SELECT column_name FROM information_schema.columns WHERE "
        f"table_schema = '{database_name}' "
        f"AND table_name = '{table_name}'")
    result = session.execute(sql_statement)
    columns = [row[0] for row in result]
    return columns


def get_all_columns_of_model(engine: Engine, model) -> list[DbColumnInfo]:
    """
    Get all columns of SqLAlchemy model
    :_type engine: sqlalchemy.engine.Engine
    :_type model: sqlalchemy.ext.declarative.declarative_base
    :param model:
    :return:
    """
    return [DbColumnInfo(engine, c) for c in model.__table__.columns]


def extract_not_exist_columns_of_model(engine, model) -> list:
    """
    :param engine:
    :param database_name:
    :return:
    """

    pass


def is_exist_table(session: Session, database_name: str, table_name: str) -> bool:
    """
    Use session to check if table is exist
    :_type session: sqlalchemy.orm.session.Session
    :_type database_name: str
    :_type table_name: str
    :param session:
    :param database_name:
     :param table_name:
      :return:
        """
    switch_database(session, database_name)
    sql_statement = text(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{database_name}' "
        f"AND table_name = '{table_name}'")
    result = session.execute(sql_statement)
    session.commit()

    if result.rowcount > 0:
        return True
    else:
        return False


def create_table_if_not_exist(session: Session, model, database_name: str) -> None:

    try:
        if not is_exist_table(session, database_name, model.__tablename__):
            model.__table__.create(session.bind.engine)
        else:
            columns = get_all_columns_of_model(session.bind.engine, model)
            columns_in_table = get_all_columns_of_table(session, database_name, model.__tablename__)
            columns_not_exist = [c for c in columns if c.db_column_name not in columns_in_table]
            for column in columns_not_exist:
                sql_statement = text(
                    f"ALTER TABLE {column.table_name} ADD COLUMN {column.db_column_name} {column.column_type}")
                session.execute(sql_statement)

            session.commit()
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        raise Exception(f"Error in create table {model.__tablename__}")

