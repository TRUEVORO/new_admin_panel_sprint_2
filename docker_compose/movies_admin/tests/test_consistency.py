import os
import sqlite3
from dataclasses import fields

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from sqlite_to_postgres import movies_mapper


@pytest.fixture
def connect_dbs():
    """Соединение с базами данных."""
    load_dotenv()

    dsl = {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('DB_HOST', 'db'),
        'port': os.environ.get('DB_PORT', 5432),
    }

    sql_path = os.environ.get('SQLITE_PATH')

    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    pg_cursor = pg_conn.cursor()

    sqlite_conn = sqlite3.connect(sql_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()

    yield pg_cursor, sqlite_cursor

    pg_conn.close()
    sqlite_conn.close()


def test_count_recs(connect_dbs):
    """Проверка количества записей в таблицах бд."""
    pg_cursor, sqlite_cursor = connect_dbs

    query = 'SELECT COUNT(id) FROM {0};'

    for table in movies_mapper.keys():
        pg_cursor.execute(query.format(f'content.{table}'))
        pg_count = pg_cursor.fetchone()[0]

        sqlite_cursor.execute(query.format(table))
        sql_count = sqlite_cursor.fetchone()[0]

        assert pg_count == sql_count


def test_check_data(connect_dbs):
    """Проверка данных в таблицах бд."""
    pg_cursor, sqlite_cursor = connect_dbs

    query = 'SELECT {0} FROM {1} ORDER BY (id);'

    for table, row_type in movies_mapper.items():
        col_names = [i.name for i in fields(row_type)]
        if 'created' in col_names:
            col_names.remove('created')
        if 'modified' in col_names:
            col_names.remove('modified')

        pg_cursor.execute(query.format(', '.join(col_names), f'content.{table}'))
        pg_data = [dict(i) for i in pg_cursor.fetchall()]

        sqlite_cursor.execute(query.format(', '.join(col_names), table))
        sql_data = [dict(i) for i in sqlite_cursor.fetchall()]

        assert pg_data == sql_data
