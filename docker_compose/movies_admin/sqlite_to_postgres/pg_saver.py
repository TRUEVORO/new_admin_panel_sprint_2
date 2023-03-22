from collections.abc import Generator
from dataclasses import fields

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch


class PostgresSaver:
    """Класс для сохранения данных в БД (Postgres)."""

    def __init__(self, connection: _connection):
        self.conn = connection
        self.cursor = connection.cursor()

    @staticmethod
    def _create_query(table: str, cols: str, values: str) -> str:
        """Создание SQL-запроса."""
        return 'INSERT INTO content.{0} ({1}) VALUES ({2}) ON CONFLICT (id) DO NOTHING;'.format(table, cols, values)

    def _make_insert_query(self, input_data: dict[str, list]) -> None:
        """Выполнение SQL-запроса."""
        table = tuple(input_data.keys())[0]
        cols = [field.name for field in fields(input_data.get(table)[0])]
        args = ', '.join(['%s'] * len(cols))
        values = [[getattr(data, field.name) for field in fields(data)] for data in input_data.get(table)]
        query = self._create_query(table, ', '.join(cols), args)
        execute_batch(self.cursor, query, values, page_size=500)

    def save_all_data(self, data: Generator[dict]) -> None:
        """Сохранение данных в БД (Postgres)."""
        for batch in data:
            self._make_insert_query(batch)
            self.conn.commit()
