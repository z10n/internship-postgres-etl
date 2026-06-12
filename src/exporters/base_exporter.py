import json
import logging
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

class Exporter:
    """Экспортирует результаты аналитики в JSON или XML."""
    SUPPORTED_FORMATS = ("json", "xml")

    def export(self, data: list[dict[str, Any]], format: str, output_path: str) -> None:
        # 1. Приводим формат к нижнему регистру для надежности (защита от "JSON", "Json")
        fmt = format.lower()
        
        # 2. Проверяем, поддерживается ли запрошенный формат
        # Если нет — сразу падаем с понятной ошибкой (Fail Fast)
        if fmt not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: '{format}'. "
                f"Supported formats: {self.SUPPORTED_FORMATS}"
            )
        
        # 3. Создаём объект Path из строки пути
        path = Path(output_path)
        
        # 4. Автоматически создаём родительские директории, если их нет
        # parents=True — создаёт всю цепочку папок (как mkdir -p)
        # exist_ok=True — не падает, если папка уже существует
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 5. Выбираем нужный приватный метод в зависимости от формата
        # Используем словарь вместо if/elif — это чище и легче расширять
        exporters = {
            "json": self._export_json,
            "xml": self._export_xml,
        }
        
        # 6. Вызываем соответствующий метод экспорта
        # Передаём данные и путь к файлу
        exporters[fmt](data, path)
        
        # 7. Логируем успешное завершение с количеством записей и путём
        logger.info(f"Exported {len(data)} records to {output_path} ({fmt})")

    def _export_json(self, data: list[dict[str, Any]], path: Path) -> None:
        # 1. Открываем файл для записи в текстовом режиме с кодировкой UTF-8
        # encoding="utf-8" критично: без него на Windows может использоваться
        # системная кодировка (cp1251), и кириллица/спецсимволы сломают файл
        with open(path, "w", encoding="utf-8") as f:
            
            # 2. Сериализуем список словарей в JSON и пишем прямо в файл
            json.dump(
                data,           # Объект для сериализации (наш список результатов)
                f,              # Файловый объект-приёмник (пишем напрямую, без промежуточной строки)
                indent=2,       # Отступ в 2 пробела для читаемости человеком
                                # Без этого весь JSON будет в одну строку
                ensure_ascii=False,  # НЕ экранировать не-ASCII символы
                                     # True (по умолчанию): "Привет" → "\u041f\u0440\u0438\u0432\u0435\u0442"
                                     # False: "Привет" остаётся как "Привет"
                default=str     # Функция-обработчик для несериализуемых типов
                                # datetime, Decimal, UUID и т.д. → преобразуются через str()
                                # Без этого json.dump выбросит TypeError на первом же сложном типе
            )
    
    @staticmethod
    def _sanitize_tag(name: str) -> str:
        """Превращает произвольную строку в валидное имя XML-тега."""
        # Заменяем всё, кроме букв, цифр, подчёркиваний и дефисов
        tag = re.sub(r"[^a-zA-Z0-9_\-]", "_", str(name))
        # Если начинается с цифры или пустая — добавляем префикс
        if not tag or tag[0].isdigit():
            tag = f"field_{tag}"
        return tag

    def _export_xml(self, data: list[dict[str, Any]], path: Path) -> None:
        root = ET.Element("results")
        
        for record in data:
            record_elem = ET.SubElement(root, "record")
            
            for key, value in record.items():
                # ✅ Используем санитизированное имя тега
                safe_key = self._sanitize_tag(key)
                field_elem = ET.SubElement(record_elem, safe_key)
                field_elem.text = str(value) if value is not None else ""
        
        tree = ET.ElementTree(root)
        tree.write(str(path), encoding="unicode", xml_declaration=True, method="xml")