import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class JsonLoader:
    @staticmethod
    def load(file_path: str) -> list[dict[str, Any]]:
        """Load and validate JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of dictionaries with data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not .json or root element is not array
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() != ".json":
            raise ValueError(f"Expected .json file, got: {path.suffix}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError(
                f"Expected JSON array in {file_path}, "
                f"got {type(data).__name__}"
            )
        
        logger.info(f"Loaded {len(data)} records from {file_path}")
        
        return data