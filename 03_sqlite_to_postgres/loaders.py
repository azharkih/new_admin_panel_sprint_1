from typing import Generator

from pydantic import BaseModel

from models import MOVIES_MODELS


class SQLiteLoader:
    def __init__(self, connection):
        self.connection = connection

    def load_movies(self) -> Generator[str, list[BaseModel], None]:
        """Метод извлечения данных о фильмах."""

        for table_name in self.tables_list:
            model = MOVIES_MODELS.get(table_name)
            if not model:
                continue
            yield table_name, self.get_data(table_name, model)

    @property
    def tables_list(self) -> list[str]:
        """Метод получения списка таблиц."""

        curs = self.connection.cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [data[0] for data in curs.fetchall()]

    def get_data(self, table_name, model) -> list[BaseModel]:
        """Метод получения данных из таблицы."""

        curs = self.connection.cursor()
        curs.execute(f"SELECT * FROM {table_name};")
        columns = [column[0] for column in curs.description]
        return [model(**dict(zip(columns, data))) for data in curs.fetchall()]
