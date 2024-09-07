
from sqldb.__info__ import IndexInfo, __get_all_indexes_in_code_model__
from sqlalchemy.sql import text
__cache_db_index__ = dict()
def __get_all_indexes_in_database__(session_instance, table_name) -> list[IndexInfo]:
    """
    This method is used to get all indexes in a table in a database.
    :param session_instance:
    :param table_name:
    :return:
    """
    if __cache_db_index__.get(table_name) is not None:
        return __cache_db_index__[table_name]

    sql_get_indexes = text(
        f"SELECT INDEX_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{session_instance.bind.db_name}'")
    indexes = session_instance.execute(sql_get_indexes).fetchall()
    index_info_list = []
    for index in indexes:
        index_info = IndexInfo(index[0], [index[1]])
        index_info_list.append(index_info)
    # cache
    __cache_db_index__[table_name] = index_info_list
    return index_info_list

def __synchronize_all_indexes_mysql__(session_instance, entity, table_name):
    """
    This method is used to synchronize all indexes  between code model and database.
    :param session_instance:
    :param entity:
    :param table_name:
    :return:
    """
    db_index: list[IndexInfo] = __get_all_indexes_in_database__(session_instance, table_name)
    model_index: list[IndexInfo] = __get_all_indexes_in_code_model__(entity)
    raise NotImplementedError("Not implemented for MySQL")

def __synchronize_session_with_code_model_mysql__(session_instance, entity, table_name,db_name):
    sql_get_column_names = text(
        f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{db_name}'")
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
    __synchronize_all_indexes_mysql__(session_instance, entity, table_name)
