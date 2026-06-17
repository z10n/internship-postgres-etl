"""Module for managing PostgreSQL connection and write operations."""

import logging
from contextlib import contextmanager
from typing import Any

import psycopg2
from psycopg2.extras import execute_values

from config.settings import Settings

logger = logging.getLogger(__name__)


class DatabaseConnector:
    """Manages database connection and provides data operations."""

    def __init__(self, settings: Settings):
        self.settings = settings

    @contextmanager
    def get_connection(self):
        """Context manager for safe connection handling.
        
        Automatically commits on success and rolls back on error.
        Ensures connection is closed.
        """
        conn = None
        try:
            logger.info("Establishing connection to PostgreSQL...")
            conn = psycopg2.connect(
                dbname=self.settings.postgres_db,
                user=self.settings.postgres_user,
                password=self.settings.postgres_password,
                host="db",
                port="5432",
            )
            logger.info("Connection established successfully.")
            yield conn
            conn.commit()
            logger.info("Transaction committed successfully.")
        except Exception as e:
            if conn:
                logger.error("Error occurred. Rolling back.")
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.info("Database connection closed.")

    def bulk_insert(
        self,
        conn,
        table: str,
        columns: tuple[str, ...],
        data: list[dict[str, Any]],
    ) -> None:
        """Bulk insert data using execute_values.
        
        Args:
            conn: Active database connection.
            table: Table name.
            columns: Tuple of column names in database.
            data: List of dictionaries with data.
        """
        if not data:
            logger.warning(f"No data to insert into table '{table}'.")
            return

        # Mapping: if data has 'room' key but database column is 'room_id'
        db_columns = tuple("room_id" if c == "room" else c for c in columns)
        data_keys = tuple("room" if c == "room_id" else c for c in db_columns)

        logger.info(f"Inserting {len(data)} records into table '{table}'...")

        # Create table if it doesn't exist (for convenience)
        with conn.cursor() as cur:
            if table == "rooms":
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS rooms (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(255) NOT NULL
                    )
                """)
            elif table == "students":
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        birthday DATE NOT NULL,
                        sex VARCHAR(10) NOT NULL,
                        room_id INTEGER REFERENCES rooms(id)
                    )
                """)

        # Extract values from dictionaries in correct order
        values = [tuple(row.get(k) for k in data_keys) for row in data]

        # Build SQL query with actual column names from database
        columns_str = ", ".join(db_columns)
        placeholders_str = ", ".join(["%s"] * len(db_columns))
        query = f"""
            INSERT INTO {table} ({columns_str})
            VALUES %s
            ON CONFLICT (id) DO NOTHING
        """

        with conn.cursor() as cur:
            execute_values(cur, query, values)

        logger.info(f"Data successfully inserted into '{table}'.")