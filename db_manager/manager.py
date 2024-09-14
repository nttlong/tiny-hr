"""
This package contains all functions and classes related to database management.

"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db_manager.db_column_info import DbColumnInfo
from typing import Iterator

# Define  a variable storing the global all database is existing
# everytime when use use_db of DbSession
# it will check if database is not exist it automatically create it
# and cache if in dictionary call __db_check__

__db_check__ = {}
#
__table_check__: dict[str, dict] = {}


def __get_column_info_from_columns_of_model__(session:Session, columns) -> Iterator['DbColumnInfo']:
    """
    This method returns an iterator of DbColumnInfo objects for the given model.
    columns: sqlalchemy.sql.schema.ColumnCollection
    :param columns:
    :return:
    """
    for column in columns:
        yield DbColumnInfo(engine=session.bind, column=column)

def __get_column_info_from_table_name__(session:Session, table_name) -> Iterator['DbColumnInfo']:
    """
    This method returns an iterator of DbColumnInfo objects for the given table name.
    :param table_name:
    :return:
    """
    # execute the query to get the column names,
    # data types, data _type sizes, and other information
    # for the given table name
    sql_stmt = text(f"SELECT "
                    f"column_name, "
                    f"data_type, "
                    f"character_maximum_length, "
                    f"numeric_precision, "
                    f"numeric_scale, "
                    f"is_nullable FROM information_schema.columns WHERE table_name = '{table_name}'")
    result = session.bind.execute(sql_stmt)
    for row in result:
        yield DbColumnInfo(
            column_name=row[0],
            data_type=row[1],
            character_maximum_length=row[2],
            numeric_precision=row[3],
            numeric_scale=row[4],

        )

def get_column_info(session: Session, model_or_table_name) -> Iterator['DbColumnInfo']:
        """
        This method returns an iterator of DbColumnInfo objects for the given model.
        :param model_or_table_name:
        :return:
        """
        if isinstance(model_or_table_name, str):
            # developer passed in a table name as a string
            # run sql query to get the column names, data types,
            # data _type sizes, and other information   for the given table name
            return __get_column_info_from_table_name__(
                session=session,
                table_name=model_or_table_name
            )
        else:
            # developer passed in a model as an argument
            # get the table name from the model
            return __get_column_info_from_columns_of_model__(
                session=session,
                columns =model_or_table_name.__table__.columns
            )

def create_database_if_not_exist(session:Session, db_name):
    """
    This method creates a new database with the given name.
    :param db_name:
    :return:
    """
    sql_stmt = text(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    session.execute(sql_stmt)

def use_db(session:Session, db_name)->Session:
    """
    This method is used to switch to the given database.
    Also it will check if database is not exist it automatically create it.
    and cache if in dictionary call __db_check__
    and hold the database name in database_name attribute of session.
    :param db_name:
    :return:
    """

    # check if db_name is already exist in __db_check__ if not call create_database_if_not_exist
    # then use_db

    if not __db_check__.get(db_name):
        create_database_if_not_exist(session,db_name)
        __db_check__[db_name] = True

    sql_stmt = text(f"USE {db_name}")
    session.execute(sql_stmt)

    return session