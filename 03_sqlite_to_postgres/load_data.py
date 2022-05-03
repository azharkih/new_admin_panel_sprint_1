import sqlite3

from psycopg2.extensions import connection as _connection

from loaders import SQLiteLoader
from savers import PostgresSaver
from db_managers import get_sqlite_conn, get_pg_conn


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with get_sqlite_conn('db.sqlite') as sqlite_conn, get_pg_conn() as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
