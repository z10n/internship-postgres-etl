import pytest
from unittest.mock import MagicMock
from src.db.queries import AnalyticsQueries

def test_get_mixed_sex_rooms():
    """Verify that the query executes and returns correct data."""
    # 1. Arrange: Create a fake connection and fake cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Mock the context manager behavior (with conn.cursor() as cur:)
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Mock the database response (list of dicts, as returned by RealDictCursor)
    fake_db_response = [
        {"room_name": "Room 101"},
        {"room_name": "Room 102"}
    ]
    mock_cursor.fetchall.return_value = fake_db_response

    # 2. Act: Call the tested method, passing the fake connection
    result = AnalyticsQueries.get_mixed_sex_rooms(mock_conn)

    # 3. Assert: Verify the result
    assert result == fake_db_response
    assert len(result) == 2
    
    # Verify behavior: ensure the cursor was actually called
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()