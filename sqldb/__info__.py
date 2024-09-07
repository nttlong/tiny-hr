class IndexInfo:
    def __init__(self, name, columns, is_unique=False, is_primary=False):
        self.name = name
        self.columns = columns
        self.is_unique = is_unique
        self.is_primary = is_primary

__cache_model_index__ = dict()
def __get_all_indexes_in_code_model__(entity) -> list[IndexInfo]:
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