import os
import sqlite3
from contextlib import closing, contextmanager

import psycopg2
from dotenv import load_dotenv
from pg_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_extr import SQLiteExtractor


@contextmanager
def conn_sqlite(db_path: str):
    """Контекстный менеджер для закрытия соединения SQLite."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_connection: _connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_connection)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    load_dotenv()

    sql_path = os.environ.get('SQLITE_PATH')

    dsl = {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('DB_HOST', 'db'),
        'port': os.environ.get('DB_PORT', 5432),
    }

    with conn_sqlite(sql_path) as sqlite_conn, closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
