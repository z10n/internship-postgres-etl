import logging
from contextlib import contextmanager
from typing import Generator
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from config.settings import Settings

logger = logging.getlogger(__name__)

class DatabaseConnector:
    def __init__(self, settings: Settings):
        self.settings = settings

    @contextmanager
    def get_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        conn = psycopg2.connect(
            host=self._settings.postgres_host,
            port=self._settings.postgres_port,
            dbname=self._settings.postgres_db,
            user=self._settings.postgres_user,
            password=self._settings.postgres_password,
            cursor_factory=RealDictCursor,
        )
        try:
            logger.info("Database connection established")
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error, rolling back: {e}")
            raise
        finally:
            conn.close()
            logger.info("Database connection closed")

    def bulk_insert(self, conn, table: str, columns: tuple[str, ...], data: list[dict]) -> None:
        """Массовая вставка данных через execute_values.
        
        Args:
            conn: Активное соединение с БД
            table: Имя таблицы
            columns: Кортеж имен колонок
            data: Список словарей с данными
        """
        if not data:
            logger.warning(f"No data to insert into {table}")
            return

        # Формируем шаблон VALUES (%s, %s, ...)
        placeholders = f"({', '.join(['%s'] * len(columns))})"
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING"
        
        # Преобразуем словари в кортежи в порядке колонок
        values = [tuple(item[col] for col in columns) for item in data]
        
        with conn.cursor() as cur:
            execute_values(cur, query, values, template=placeholders)
            logger.info(f"Inserted {len(values)} rows into {table}")        