# src/db/queries.py
from typing import Any
import psycopg2.extensions


class AnalyticsQueries:
    """Инкапсулирует все аналитические SQL-запросы.
    
    Single Responsibility: только чтение данных.
    Все вычисления выполняются на стороне PostgreSQL.
    """

    @staticmethod
    def get_students_per_room(conn: psycopg2.extensions.connection) -> list[dict[str, Any]]:
        """Количество студентов в каждой комнате."""
        query = """
            SELECT r.name AS room_name, COUNT(s.id) AS student_count
            FROM rooms r
            LEFT JOIN students s ON s.room = r.id
            GROUP BY r.id, r.name
            ORDER BY r.name;
        """
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    @staticmethod
    def get_lowest_avg_age_rooms(conn: psycopg2.extensions.connection, limit: int = 5) -> list[dict[str, Any]]:
        """Топ-N комнат с минимальным средним возрастом."""
        query = """
            SELECT r.name AS room_name, 
                   ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday)))::numeric, 2) AS avg_age
            FROM rooms r
            JOIN students s ON s.room = r.id
            GROUP BY r.id, r.name
            ORDER BY avg_age ASC
            LIMIT %s;
        """
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            return cur.fetchall()

    @staticmethod
    def get_largest_age_diff_rooms(conn: psycopg2.extensions.connection, limit: int = 5) -> list[dict[str, Any]]:
        """Топ-N комнат с максимальной разницей в возрасте."""
        query = """
            SELECT r.name AS room_name,
                   MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - 
                   MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS age_diff
            FROM rooms r
            JOIN students s ON s.room = r.id
            GROUP BY r.id, r.name
            ORDER BY age_diff DESC
            LIMIT %s;
        """
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            return cur.fetchall()

    @staticmethod
    def get_mixed_sex_rooms(conn: psycopg2.extensions.connection) -> list[dict[str, Any]]:
        """Комнаты с разнополыми студентами."""
        query = """
            SELECT r.name AS room_name
            FROM rooms r
            JOIN students s ON s.room = r.id
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
            ORDER BY r.name;
        """
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()