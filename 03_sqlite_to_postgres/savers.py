from typing import Generator

from psycopg2._psycopg import connection as _connection
from psycopg2.extras import execute_batch
from pydantic import BaseModel

from models import MOVIES_MODELS


class PostgresSaver:
    def __init__(self, connection: _connection, page_size=None):
        self.connection = connection
        self.page_size = 5000 if page_size is None else page_size

    def save_all_data(self, data: Generator[str, list[BaseModel], None]):
        """Метод сохранения всех данных в базу."""

        for table_name, table_data in data:
            self.push_data(table_name, table_data)

    def push_data(self, table_name: str, data: list[BaseModel]) -> None:
        """Метод сохранения данных в таблицу."""
        curs = self.connection.cursor()
        fields = list(MOVIES_MODELS.get(table_name).__fields__.keys())
        fields_string = ', '.join(fields)
        values_string = ', '.join('%s' for _ in range(len(fields)))
        query = (f'INSERT INTO content.{table_name} ({fields_string}) '
                 f'VALUES ({values_string}) ON CONFLICT DO NOTHING; ')
        data = [tuple(getattr(row, field) for field in fields) for row in data]
        execute_batch(curs, query, data, page_size=self.page_size)
        self.connection.commit()
