"""
This file contains the DbColumnInfo class.

The DbColumnInfo class is used to store information about a database column.
"""
from sqlalchemy.engine import Engine
class DbColumnInfo:
    def __init__(self,
                 engine: Engine | None = None,
                 column=None,
                 column_name: str | None = None,
                 table_name: str | None = None,
                 data_type:str | None = None,
                 character_maximum_length: int | None = None,
                 numeric_precision: int | None = None,
                 numeric_scale:int|None=None,):
        if engine is not None:
            if column is None:
                raise ValueError("column must be provided when engine is not None")
            self.column_name = column.compile(dialect=engine.dialect)
            self.column_type = column.type.compile(engine.dialect)
            self.table_name = column.table.name
            self.db_column_name = column.name

        else:
            _column_type = data_type
            # calculate the column type based on the data type and other parameters
            if character_maximum_length is not None:
                _column_type = f"{_column_type}({character_maximum_length})"
            elif numeric_precision is not None and numeric_scale is not None:
                _column_type = f"{_column_type}({numeric_precision},{numeric_scale})"
            self.column_type = _column_type
            self.column_name = column_name
            self.table_name = table_name



