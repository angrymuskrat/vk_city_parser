import json

from sqlalchemy import func
from sqlalchemy.types import UserDefinedType


class Vector(UserDefinedType):
    def get_col_spec(self, **kw):
        return "VECTOR"

    def bind_expression(self, bindvalue):
        return func.vector(bindvalue)

    def column_expression(self, col):
        return col

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return '[' + ', '.join(str(el) for el in value) + ']'  # Преобразование в список, если используется numpy массив
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return json.loads(value)# Преобразование обратно в numpy массив
            return value

        return process
