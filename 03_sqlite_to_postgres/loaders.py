import sqlite3
from typing import Generator

from pydantic import BaseModel

from models import MOVIES_MODELS


class SQLiteLoader:
    def __init__(self, connection, batch_size=None):
        self.connection = connection
        self.batch_size = 10000 if batch_size is None else batch_size

    def load_movies(self) -> Generator[str, list[BaseModel], None]:
        """Метод извлечения данных о фильмах."""

        for table_name in self.tables_list:
            model = MOVIES_MODELS.get(table_name)
            if not model:
                continue
            for data in self.get_data(table_name, model):
                yield table_name, data

    @property
    def tables_list(self) -> list[str]:
        """Метод получения списка таблиц."""

        curs = self.connection.cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [data[0] for data in curs.fetchall()]

    def get_data(
            self, table_name, model
    ) -> Generator[list[BaseModel], None, None]:
        """Метод получения данных из таблицы."""

        try:
            curs = self.connection.cursor()
            curs.execute(f"SELECT * FROM {table_name};")
            columns = [column[0] for column in curs.description]
        except sqlite3.Error as e:
            raise e
        while True:
            rows = curs.fetchmany(size=self.batch_size)
            if not rows:
                break
            yield [model(**dict(zip(columns, data))) for data in rows]
