import os
from abc import ABC

from dateutil import parser

import sqlite3
from datetime import datetime

import psycopg2
import pytest
from psycopg2.extras import DictCursor

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope='session')
def sqlite_conn():
    with sqlite3.connect('db.sqlite') as sqlite_conn:
        yield sqlite_conn


@pytest.fixture(scope='session')
def pg_conn():
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432)
    }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        yield pg_conn


class TableTest(ABC):
    """Базовые проверки таблиц."""

    pg_table_name = 'content.film_work'
    sqlite_table_name = 'film_work'
    matching = {'id': 'id', 'title': 'title', 'description': 'description',
                'creation_date': 'creation_date', 'rating': 'rating',
                'type': 'type', 'created': 'created_at',
                'modified': 'updated_at', 'file_path': 'file_path'}

    def test_full_load(self, sqlite_conn, pg_conn):
        """
        Проверка целостности данных между каждой парой таблиц в SQLite и
        Postgres. Проверятся количество записей в каждой таблице.
        """
        curs_sqlite = sqlite_conn.cursor()
        curs_pg = pg_conn.cursor()
        curs_pg.execute(f"SELECT count(*) FROM {self.pg_table_name};")
        curs_sqlite.execute(f"SELECT count(*) FROM {self.sqlite_table_name};")
        assert curs_sqlite.fetchall()[0][0] == curs_pg.fetchall()[0][0]

    def test_fields(self, sqlite_conn, pg_conn):
        """
        Проверка содержимого записей внутри каждой таблицы. Проверяется, что
        все записи из PostgreSQL присутствуют с такими же значениями полей, как
        и в SQLite.
        """
        curs_sqlite = sqlite_conn.cursor()
        curs_sqlite.execute(f"SELECT * FROM {self.sqlite_table_name} LIMIT 1;")
        columns_sqlite = [column[0] for column in curs_sqlite.description]
        data_sqlite = dict(zip(columns_sqlite, curs_sqlite.fetchall()[0]))

        curs_pg = pg_conn.cursor()
        curs_pg.execute(f"SELECT * FROM {self.pg_table_name} "
                        f"where id = '{data_sqlite['id']}';")
        columns_pg = [column[0] for column in curs_pg.description]
        data_pg = dict(zip(columns_pg, curs_pg.fetchall()[0]))

        for field_pg, field_sqlite in self.matching.items():
            value_pg = data_pg.get(field_pg)
            value_sqlite = data_sqlite.get(field_sqlite)
            if isinstance(value_pg, datetime):
                value_sqlite = parser.parse(value_sqlite)
            assert value_sqlite == value_pg


class TestFilmWork(TableTest):
    """ Проверка таблицы film_work на корректность переноса."""

    pg_table_name = 'content.film_work'
    sqlite_table_name = 'film_work'
    matching = {'id': 'id', 'title': 'title', 'description': 'description',
                'creation_date': 'creation_date', 'rating': 'rating',
                'type': 'type', 'created': 'created_at',
                'modified': 'updated_at', 'file_path': 'file_path'}


class TestGenre(TableTest):
    """ Проверка таблицы genre на корректность переноса."""

    pg_table_name = 'content.genre'
    sqlite_table_name = 'genre'
    matching = {'id': 'id', 'name': 'name', 'description': 'description',
                'created': 'created_at', 'modified': 'updated_at'}


class TestGenreFilmWork(TableTest):
    """ Проверка таблицы genre_film_work на корректность переноса."""

    pg_table_name = 'content.genre_film_work'
    sqlite_table_name = 'genre_film_work'
    matching = {'id': 'id', 'genre_id': 'genre_id',
                'film_work_id': 'film_work_id', 'created': 'created_at'}


class TestPerson(TableTest):
    """ Проверка таблицы person на корректность переноса."""

    pg_table_name = 'content.person'
    sqlite_table_name = 'person'
    matching = {'id': 'id', 'full_name': 'full_name',
                'created': 'created_at', 'modified': 'updated_at'}


class TestPersonFilmWork(TableTest):
    """ Проверка таблицы person_film_work на корректность переноса."""

    pg_table_name = 'content.person_film_work'
    sqlite_table_name = 'person_film_work'
    matching = {'id': 'id', 'person_id': 'person_id', 'role': 'role',
                'film_work_id': 'film_work_id', 'created': 'created_at'}
