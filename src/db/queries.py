# src/db/queries.py
from typing import Any
import psycopg2.extensions


class AnalyticsQueries:
    """SQL queries for analytics."""
    
    # SQL queries as class constants
    QUERY_STUDENTS_PER_ROOM = """
        SELECT r.name AS room_name, COUNT(s.id) AS student_count
        FROM rooms r
        LEFT JOIN students s ON s.room = r.id
        GROUP BY r.id, r.name
        ORDER BY r.name;
    """
    
    QUERY_LOWEST_AVG_AGE_ROOMS = """
        SELECT r.name AS room_name, 
               ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday)))::numeric, 2) AS avg_age
        FROM rooms r
        JOIN students s ON s.room = r.id
        GROUP BY r.id, r.name
        ORDER BY avg_age ASC
        LIMIT %s;
    """
    
    QUERY_LARGEST_AGE_DIFF_ROOMS = """
        SELECT r.name AS room_name,
               MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - 
               MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS age_diff
        FROM rooms r
        JOIN students s ON s.room = r.id
        GROUP BY r.id, r.name
        ORDER BY age_diff DESC
        LIMIT %s;
    """
    
    QUERY_MIXED_SEX_ROOMS = """
        SELECT r.name AS room_name
        FROM rooms r
        JOIN students s ON s.room = r.id
        GROUP BY r.id, r.name
        HAVING COUNT(DISTINCT s.sex) > 1
        ORDER BY r.name;
    """

    @staticmethod
    def _execute_query(
        conn: psycopg2.extensions.connection, 
        query: str, 
        params: tuple = None
    ) -> list[tuple]:
        """Execute SQL query and return results.
        
        Args:
            conn: Database connection.
            query: SQL query string.
            params: Query parameters (optional).
            
        Returns:
            List of tuples with query results.
        """
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.fetchall()

    @staticmethod
    def get_students_per_room(conn: psycopg2.extensions.connection) -> list[tuple]:
        """Count of students in each room."""
        return AnalyticsQueries._execute_query(conn, AnalyticsQueries.QUERY_STUDENTS_PER_ROOM)

    @staticmethod
    def get_lowest_avg_age_rooms(conn: psycopg2.extensions.connection, limit: int = 5) -> list[tuple]:
        """Top-N rooms with the lowest average age."""
        return AnalyticsQueries._execute_query(conn, AnalyticsQueries.QUERY_LOWEST_AVG_AGE_ROOMS, (limit,))

    @staticmethod
    def get_largest_age_diff_rooms(conn: psycopg2.extensions.connection, limit: int = 5) -> list[tuple]:
        """Top-N rooms with the largest age difference."""
        return AnalyticsQueries._execute_query(conn, AnalyticsQueries.QUERY_LARGEST_AGE_DIFF_ROOMS, (limit,))

    @staticmethod
    def get_mixed_sex_rooms(conn: psycopg2.extensions.connection) -> list[tuple]:
        """Rooms with students of mixed sexes."""
        return AnalyticsQueries._execute_query(conn, AnalyticsQueries.QUERY_MIXED_SEX_ROOMS)