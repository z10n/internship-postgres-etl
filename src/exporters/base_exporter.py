import json
import logging
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

class Exporter:
    """Exports analytics results to JSON or XML."""
    SUPPORTED_FORMATS = ("json", "xml")

    def export(self, data: list[dict[str, Any]], format: str, output_path: str) -> None:
        fmt = format.lower()
        
        if fmt not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: '{format}'. "
                f"Supported formats: {self.SUPPORTED_FORMATS}"
            )
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        exporters = {
            "json": self._export_json,
            "xml": self._export_xml,
        }
        
        exporters[fmt](data, path)
        logger.info(f"Exported {len(data)} records to {output_path} ({fmt})")

    def _export_json(self, data: list[dict[str, Any]], path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                default=str
            )
    
    @staticmethod
    def _sanitize_tag(name: str) -> str:
        """Converts arbitrary string to valid XML tag name."""
        tag = re.sub(r"[^a-zA-Z0-9_\-]", "_", str(name))
        if not tag or tag[0].isdigit():
            tag = f"field_{tag}"
        return tag

    def _export_xml(self, data: list[dict[str, Any]], path: Path) -> None:
        root = ET.Element("results")
        
        for record in data:
            record_elem = ET.SubElement(root, "record")
            
            for key, value in record.items():
                safe_key = self._sanitize_tag(key)
                field_elem = ET.SubElement(record_elem, safe_key)
                field_elem.text = str(value) if value is not None else ""
        
        tree = ET.ElementTree(root)
        tree.write(str(path), encoding="unicode", xml_declaration=True, method="xml")