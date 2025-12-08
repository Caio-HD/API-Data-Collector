"""
CSV data exporter
"""

import csv
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from ..core.base_exporter import BaseExporter


class CSVExporter(BaseExporter):
    """
    Exporter for CSV format.
    
    Handles flat and nested data structures.
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize CSV exporter.
        
        Args:
            output_dir: Output directory
        """
        super().__init__(output_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def export(
        self,
        data: Any,
        filename: str,
        flatten_nested: bool = True,
        **kwargs
    ) -> str:
        """
        Export data to CSV file.
        
        Args:
            data: Data to export (list of dicts or single dict)
            filename: Output filename (will add .csv if not present)
            flatten_nested: Flatten nested structures (e.g., lists to comma-separated strings)
            **kwargs: Additional options
            
        Returns:
            Path to exported file
        """
        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename = f"{filename}.csv"
        
        file_path = self._get_file_path(filename)
        
        # Convert single dict to list
        if isinstance(data, dict):
            data = [data]
        
        if not isinstance(data, list) or len(data) == 0:
            self.logger.warning("No data to export or invalid format")
            return str(file_path)
        
        # Flatten data if needed
        if flatten_nested:
            data = [self._flatten_dict(item) for item in data]
        
        # Get all unique keys from all items
        all_keys = set()
        for item in data:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        
        fieldnames = sorted(all_keys)
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in data:
                    if isinstance(item, dict):
                        # Convert values to strings and handle None
                        row = {
                            key: self._format_value(item.get(key))
                            for key in fieldnames
                        }
                        writer.writerow(row)
            
            self.logger.info(f"Exported {len(data)} rows to {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Failed to export CSV: {e}")
            raise
    
    def _flatten_dict(self, data: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten nested dictionary structure.
        
        Args:
            data: Dictionary to flatten
            parent_key: Parent key prefix
            sep: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key, sep=sep).items())
            elif isinstance(value, list):
                # Convert list to comma-separated string
                if value and isinstance(value[0], dict):
                    # List of dicts - convert to JSON string
                    import json
                    items.append((new_key, json.dumps(value)))
                else:
                    # Simple list - join with comma
                    items.append((new_key, ', '.join(str(v) for v in value)))
            else:
                items.append((new_key, value))
        
        return dict(items)
    
    def _format_value(self, value: Any) -> str:
        """
        Format value for CSV export.
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string value
        """
        if value is None:
            return ''
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (list, dict)):
            import json
            return json.dumps(value)
        else:
            return str(value)
