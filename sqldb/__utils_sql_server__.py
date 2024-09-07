from sqlalchemy.sql import text
from sqldb.__info__ import  IndexInfo

class SQLIndexInfo:
    """
    This class is used to represent an index of a table in a database.
    After executing a SQL query to get all indexes of a table in a database, this class will be used to represent each index.
    The SQL is 'SELECT i.name,i.type_desc,i.type,i.is_unique, c.name as col_name FROM sys.indexes i JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id WHERE i.object_id = OBJECT_ID('{table_name}'
    """
    name: str
    type_desc: str
    type: str
    is_unique: bool
    col_name: str





def __synchronize_all_indexes_sqlserver__(session_instance, entity, table_name):
    """
    This method is used to synchronize all indexes of an entity of sqlalchemy with a table in a database.
    :param session_instance:
    :param entity:
    :param table_name:
    raise NotImplementedError("Not implemented for SQL Server")
    """
    cnn = session_instance.bind.connect()
    cnn.autocommit = True
    try:
        #declare sql get all indexes  index typeand related columns of table in database
        sql_get_indexes_and_columns = (f"SELECT i.name,"
                                       f"i.type_desc,"
                                       f"i.type index_type,"
                                       f"i.is_unique,"
                                       f" c.name as col_name "
                                       f"FROM sys.indexes "
                                       f"i JOIN sys.index_columns ic "
                                       f"ON i.object_id = ic.object_id AND "
                                       f"i.index_id = ic.index_id JOIN sys.columns c "
                                       f"ON ic.object_id = c.object_id AND "
                                       f"ic.column_id = c.column_id "
                                       f"WHERE i.object_id = OBJECT_ID('{table_name}')")

        indexes_in_db:list[SQLIndexInfo] = []
        for index in cnn.exec_driver_sql(sql_get_indexes_and_columns):
            sql_index_info = SQLIndexInfo()
            sql_index_info.name = index[0]
            sql_index_info.type_desc = index[1]
            sql_index_info.type = index[2]
            sql_index_info.is_unique = index[3]==1
            sql_index_info.col_name = index[4]
            indexes_in_db.append(sql_index_info)
        # group indexes by name of indexes_in_db
        indexes_in_db_grouped: list[IndexInfo] = []
        from itertools import groupby
        for info, group in groupby(indexes_in_db, lambda x: dict(
            name=x.name,
            is_unique=x.is_unique
        )):

            indexes_in_db_grouped.append(IndexInfo(
                name=info.get('name'),
                columns=[col.col_name for col in group],
                is_unique=info.get('is_unique'),
                is_primary=False,
            ))
        print(indexes_in_db_grouped)

        indexes_in_db = {index.name: index for index in indexes_in_db}
        print(indexes_in_db)



        #get all indexes of entity in code model
        indexes_in_code_model = [index.name for index in entity.__table__.indexes]
        #get indexes to be created
        indexes_to_be_created = list(set(indexes_in_code_model) - set(indexes_in_db))
    except:
        cnn.rollback()
        raise
    finally:
        cnn.close()


    raise NotImplementedError("Not implemented for SQL Server")




def __synchronize_session_with_code_model_sqlserver__(session_instance, entity, table_name, db_name):
    """
    This method is used to synchronize an entity of sqlalchemy with a table in a database.
    :param session_instance:
    :param entity:
    :param table_name:
    :param db_name:
    :return:
    """

    # get all column names of table in database by executing a SQL server query
    sql_get_column_names = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'dbo'"
    sql_get_column_names = text(sql_get_column_names)
    # sql_get_column_names = text(
    #     f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{db_name}'")
    column_names_in_db = [row[0] for row in session_instance.execute(sql_get_column_names).fetchall()]
    # get all column names of table in code model
    column_names_in_code_model = [column.name for column in entity.__table__.columns]
    sync_cols = list(set(column_names_in_code_model) - set(column_names_in_db))

    for col in sync_cols:
        # create column in database
        cnn = session_instance.bind.connect()
        cnn.autocommit = True
        try:
            col_type = entity.__table__.columns[col].type.compile(dialect=session_instance.bind.dialect)
            #sql alter table add column for SQL server
            sql_add_column = f"ALTER TABLE {table_name} ADD {col} {col_type}"
            cnn.exec_driver_sql(sql_add_column)
            # get SQL server default value by
            # using the default value  of the   column in sqlalchemy model


            default_value = entity.__table__.columns[col].default.arg
            sql_set_default_value = None
            if default_value == True:
                sql_set_default_value = 1
            elif default_value == False:
                sql_set_default_value = 0
            elif isinstance(default_value, str):
                sql_set_default_value = f"'{default_value}'"
            else:
                raise NotImplementedError(f"Default value of type {type(default_value)} is not supported for SQL Server")

            if default_value is not None:
                #sql alter table alter column for SQL server
                sql_set_default = f"ALTER TABLE {table_name} ADD CONSTRAINT DF_{table_name}_{col} DEFAULT {sql_set_default_value} FOR {col}"
                cnn.exec_driver_sql(sql_set_default)
            cnn.commit()
        except Exception as e:
            cnn.rollback()
        finally:
            cnn.close()

    __synchronize_all_indexes_sqlserver__(session_instance, entity, table_name)
