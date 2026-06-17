import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.exporters.base_exporter import Exporter

@patch("src.exporters.base_exporter.json.dump")
@patch("src.exporters.base_exporter.Path.mkdir")
def test_export_json_calls_correct_methods(mock_mkdir, mock_json_dump):
    """Verify that JSON export calls the correct functions with the right arguments."""
    # Arrange
    exporter = Exporter()
    test_data = [{"room_name": "Room 1", "student_count": 5}]
    output_path = "output/test_results.json"
    
    # Act
    exporter.export(test_data, "json", output_path)
    
    # Assert
    # 1. Verify that directories were created
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    # 2. Verify that json.dump was called with our data and correct flags
    # mock_open() simulates the open() function
    mock_json_dump.assert_called_once()
    
    # Get the arguments with which json.dump was called
    call_args = mock_json_dump.call_args
    
    assert call_args[0][0] == test_data  # First positional argument is our data
    assert call_args[1]["indent"] == 2   # Keyword argument indent
    assert call_args[1]["ensure_ascii"] is False # Keyword argument ensure_ascii