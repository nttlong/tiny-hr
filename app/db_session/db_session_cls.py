"""
This package contains the database session management.
It declares a class DbSession is inheriting from sqlalchemy.orm.session.Session.
Some Dunder methods are defined to manage the session in a context manager.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .db_column_info import DbColumnInfo
from typing import Iterator

# Define  a variable storing the global all database is existing
# everytime when use use_db of DbSession
# it will check if database is not exist it automatically create it
# and cache if in dictionary call __db_check__

__db_check__ = {}



class DbSession(Session):
    """
    This class is inheriting from sqlalchemy.orm.session.Session.
    """

    def __init__(self, db_engine):
        super().__init__(bind=db_engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type:
            self.rollback()
            return False

        else:
            self.commit()
            return True

    def commit(self):
        try:
            super().commit()
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        super().rollback()
        self.close()

    def close(self):
        super().close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return f"<DbSession(bind={self.bind})>"

    def __str__(self):
        return f"DbSession(bind={self.bind})"

    def __unicode__(self):
        return f"DbSession(bind={self.bind})"

    def __hash__(self):
        return hash(self.bind)

    def __eq__(self, other):
        return self.bind == other.bind

    def __ne__(self, other):
        return not self.__eq__(other)

    def execute(self, *args, **kwargs):
        return super().execute(*args, **kwargs)

    def use_db(self, db_name):

        # check if db_name is already exist in __db_check__ if not call create_database_if_not_exist
        # then use_db

        if not __db_check__.get(db_name):
            self.create_database_if_not_exist(db_name)
            __db_check__[db_name] = True

        sql_stmt = text(f"USE {db_name}")
        self.bind.execute(sql_stmt)
        return self

    def get_column_info(self, model_or_table_name) -> Iterator['DbColumnInfo']:
        """
        This method returns an iterator of DbColumnInfo objects for the given model.
        :param model_or_table_name:
        :return:
        """
        if isinstance(model_or_table_name, str):
            # developer passed in a table name as a string
            # run sql query to get the column names, data types,
            # data type sizes, and other information   for the given table name
            return self.__get_column_info_from_table_name__(table_name=model_or_table_name)
        else:
            # developer passed in a model as an argument
            # get the table name from the model
            return self.__get_column_info_from_columns_of_model__(columns=model_or_table_name.__table__.columns)

    def __get_column_info_from_table_name__(self, table_name) -> Iterator['DbColumnInfo']:
        """
        This method returns an iterator of DbColumnInfo objects for the given table name.
        :param table_name:
        :return:
        """
        # execute the query to get the column names,
        # data types, data type sizes, and other information
        # for the given table name
        sql_stmt = text(f"SELECT "
                        f"column_name, "
                        f"data_type, "
                        f"character_maximum_length, "
                        f"numeric_precision, "
                        f"numeric_scale, "
                        f"is_nullable FROM information_schema.columns WHERE table_name = '{table_name}'")
        result = self.bind.execute(sql_stmt)
        for row in result:
            yield DbColumnInfo(
                column_name=row[0],
                data_type=row[1],
                character_maximum_length=row[2],
                numeric_precision=row[3],
                numeric_scale=row[4],

            )

    def __get_column_info_from_columns_of_model__(self, columns) -> Iterator['DbColumnInfo']:
        """
        This method returns an iterator of DbColumnInfo objects for the given model.
        columns: sqlalchemy.sql.schema.ColumnCollection
        :param columns:
        :return:
        """
        for column in columns:
            yield DbColumnInfo(engine=self.bind, column=column)

    def create_database_if_not_exist(self, db_name):
        """
        This method creates a new database with the given name.
        :param db_name:
        :return:
        """
        sql_stmt = text(f"CREATE DATABASE {db_name} IF NOT EXISTS")
        self.bind.execute(sql_stmt)


if __name__ == '__main__':
    pass
