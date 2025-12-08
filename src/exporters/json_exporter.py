"""
JSON data exporter
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from ..core.base_exporter import BaseExporter


class JSONExporter(BaseExporter):
    """
    Exporter for JSON format.
    
    Supports exporting single objects or lists to JSON files.
    """
    
    def __init__(self, output_dir: str = "output", indent: int = 2):
        """
        Initialize JSON exporter.
        
        Args:
            output_dir: Output directory
            indent: JSON indentation level
        """
        super().__init__(output_dir)
        self.indent = indent
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def export(
        self,
        data: Any,
        filename: str,
        ensure_ascii: bool = False,
        **kwargs
    ) -> str:
        """
        Export data to JSON file.
        
        Args:
            data: Data to export (dict, list, or any JSON-serializable object)
            filename: Output filename (will add .json if not present)
            ensure_ascii: Ensure ASCII encoding
            **kwargs: Additional options
            
        Returns:
            Path to exported file
        """
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename = f"{filename}.json"
        
        file_path = self._get_file_path(filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    data,
                    f,
                    indent=self.indent,
                    ensure_ascii=ensure_ascii,
                    default=str  # Handle non-serializable objects
                )
            
            self.logger.info(f"Exported data to {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Failed to export JSON: {e}")
            raise
    
    def export_multiple(
        self,
        data_dict: Dict[str, Any],
        prefix: str = "",
        **kwargs
    ) -> List[str]:
        """
        Export multiple datasets to separate JSON files.
        
        Args:
            data_dict: Dictionary mapping names to data
            prefix: Optional prefix for filenames
            **kwargs: Additional options
            
        Returns:
            List of exported file paths
        """
        exported_files = []
        
        for name, data in data_dict.items():
            filename = f"{prefix}{name}.json" if prefix else f"{name}.json"
            file_path = self.export(data, filename, **kwargs)
            exported_files.append(file_path)
        
        return exported_files
