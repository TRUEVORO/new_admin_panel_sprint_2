import sqlite3
from collections.abc import Generator

from dataclass_templates import movies_mapper


class SQLiteExtractor:
    """Класс для получения данных из БД SQLite3."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def _make_query(self, table: str) -> None:
        """Выполнение SQL-запроса."""
        self.cursor.execute('SELECT * FROM {0};'.format(table))

    def _fetch_data_gen(self) -> Generator[list]:
        """Получение данных в заданном количестве."""
        while True:
            data = [dict(i) for i in self.cursor.fetchmany(size=500)]
            if not data:
                break
            yield data

    @staticmethod
    def _create_data(table: str, row_type: type, batch: list[dict]) -> list[object]:
        """Создание массива данных по заданным датаклассам."""
        if table in ['genre_film_work', 'person_film_work']:
            data = [row_type(created=row.pop('created_at'), **row) for row in batch]
        else:
            if table == 'film_work':
                for row in batch:
                    del row['file_path']
            data = [row_type(created=row.pop('created_at'), modified=row.pop('updated_at'), **row) for row in batch]
        return data

    def extract_movies(self) -> Generator[dict]:
        """Выгрузка данных из БД (SQLite3)."""
        for table_name, row_type in movies_mapper.items():
            self._make_query(table=table_name)
            for batch in self._fetch_data_gen():
                yield {table_name: self._create_data(table=table_name, row_type=row_type, batch=batch)}
