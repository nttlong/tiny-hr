
"""
This dictionary is used to check if table is already exist or not.
The key is database name and value is dictionary of table name and boolean value.
Example:
__table_check__ = {
    'db1': {
        'table1': True,
        'table2': False
        },
        
    'db2': {
        'table1': True,
        'table2': True
        }
    
}
        
"""


class DbSession(Session):
    """
    This class is inheriting from sqlalchemy.orm.session.Session.
    """

    def __init__(self, db_engine):
        super().__init__(bind=db_engine)
        self.__database_name__ = None

    @property
    def __get_database_name__(self):
        """
        Read-only property to get the database name of the current session.
        :return:
        """
        return self.__database_name__


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











    def create_table_if_not_exist(self, model):
        """
        This method creates a new table with the given model.
        :param model:
        :return:
        """
        # the first get table name from model and check if it in __table_check__
        # if not create table and add it in __table_check__
        # if exist return
        table_name = model.__table__.name
        if __table_check__.get(self.__database_name__, {}).get(table_name):
            return

        model.__table__.create(self.bind, checkfirst=True)
        # get all columns in database
        columns_in_database = self.__get_column_info_from_table_name__(table_name=table_name)
        # get all columns in model
        columns_in_model = self.__get_column_info_from_columns_of_model__(columns=model.__table__.columns)
        # get all columns in model but not in database
        columns_to_create = [column for column in columns_in_model if column not in columns_in_database]
        # create new table with new columns
        if columns_to_create:
            new_table = model.__table__.tometadata(self.bind)

            # add new columns in __table_check__
            for column in columns_to_create:
                self.__create_column_in_table__(table_name=table_name, column=column)
    def __create_column_in_table__(self, table_name, column):
        """
        This method creates a new column in the given table.
        :param table_name:
        :param column:
        :return:
        """
        # create new column in table
        column.create(self.bind, checkfirst=True)
        # add new column in __table_check__




if __name__ == '__main__':
    pass
