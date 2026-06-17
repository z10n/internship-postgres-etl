import pytest
from pathlib import Path
from src.loaders.json_loader import JsonLoader

def test_load_file_not_found():
    """Check that Loader raises FileNotFoundError for a non-existent file."""
    # Arrange
    fake_path = "non_existent_file.json"
    
    # Act & Assert
    # pytest.raises catches the specific exception. If not raised, the test fails.
    with pytest.raises(FileNotFoundError, match="File not found"):
        JsonLoader.load(fake_path)

def test_load_invalid_extension(tmp_path):
    """Check that Loader rejects files without the .json extension."""
    # Arrange: create a temporary file with an incorrect extension
    fake_file = tmp_path / "data.txt"
    fake_file.write_text('[{"id": 1}]')
    
    # Act & Assert
    with pytest.raises(ValueError, match="Expected .json file"):
        JsonLoader.load(str(fake_file))