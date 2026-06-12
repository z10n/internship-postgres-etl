import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class JsonLoader:
    @staticmethod
    def load(file_path: str) -> list[dict[str, Any]]:
        """Загружает и валидирует JSON-файл.
        
        Args:
            file_path: Путь к JSON-файлу
            
        Returns:
            Список словарей с данными
            
        Raises:
            FileNotFoundError: Если файл не существует
            ValueError: Если файл не .json или корневой элемент не массив
        """
        path = Path(file_path)
        
        # 1. Проверка существования
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # 2. Проверка расширения
        if path.suffix.lower() != ".json":
            raise ValueError(f"Expected .json file, got: {path.suffix}")
        
        # 3. Чтение файла
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 4. Валидация структуры (Fail Fast!)
        if not isinstance(data, list):
            raise ValueError(
                f"Expected JSON array in {file_path}, "
                f"got {type(data).__name__}"
            )
        
        # 5. Логирование результата
        logger.info(f"Loaded {len(data)} records from {file_path}")
        
        return data 