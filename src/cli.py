"""ETL pipeline entry point."""
import argparse
import logging
import sys

from config.settings import Settings
from src.db.connector import DatabaseConnector
from src.db.queries import AnalyticsQueries
from src.exporters.base_exporter import Exporter
from src.loaders.json_loader import JsonLoader

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ETL: Load students/rooms JSON into PostgreSQL and run analytics"
    )
    parser.add_argument("--students", required=True, help="Path to students.json")
    parser.add_argument("--rooms", required=True, help="Path to rooms.json")
    parser.add_argument(
        "--format",
        required=True,
        choices=["json", "xml"],
        help="Output format: json or xml",
    )
    return parser.parse_args()


def setup_logging(level: str) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


def main() -> None:
    """Orchestrate the entire ETL pipeline."""
    args = parse_args()
    settings = Settings()
    setup_logging(settings.log_level)

    logger.info("Starting ETL pipeline")

    loader = JsonLoader()
    students = loader.load(args.students)
    rooms = loader.load(args.rooms)

    connector = DatabaseConnector(settings)
    with connector.get_connection() as conn:
        # IMPORTANT: Insert rooms first due to foreign key constraint!
        connector.bulk_insert(conn, "rooms", ("id", "name"), rooms)
        connector.bulk_insert(
            conn,
            "students",
            ("id", "name", "birthday", "sex", "room"),
            students,
        )

        results: list[dict] = []
        results.extend(AnalyticsQueries.get_students_per_room(conn))
        results.extend(AnalyticsQueries.get_lowest_avg_age_rooms(conn))
        results.extend(AnalyticsQueries.get_largest_age_diff_rooms(conn))
        results.extend(AnalyticsQueries.get_mixed_sex_rooms(conn))

    exporter = Exporter()
    output_path = f"output/results.{args.format}"
    exporter.export(results, args.format, output_path)

    logger.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    main()