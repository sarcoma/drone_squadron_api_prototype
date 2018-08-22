from abc import ABCMeta

from sqlalchemy.engine import ResultProxy


class BaseApi(metaclass=ABCMeta):

    def __init__(self, table):
        self.table = table

    def get(self):
        with self.table() as crud:
            result = crud.select()  # type: ResultProxy
            data = result.fetchall()
        return data

    def get_by_id(self, item_id):
        with self.table() as crud:
            result = crud.select_by_id(item_id)  # type: ResultProxy
            data = result.fetchone()
        return data

    def post(self, data: object) -> object:
        with self.table() as crud:
            result = crud.insert(**data)  # type: ResultProxy
            last_id = result.inserted_primary_key
        return last_id

    def put(self, item_id, data):
        with self.table() as crud:
            result = crud.update(item_id=item_id, **data)  # type: ResultProxy
            data = result.last_updated_params()
        return data

    def delete(self, item_id):
        with self.table() as crud:
            result = crud.delete(item_id=item_id)  # type: ResultProxy
            matched_rows = result.rowcount
        return matched_rows

