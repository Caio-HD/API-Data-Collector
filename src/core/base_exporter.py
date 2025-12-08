"""
Base exporter class for data export
"""

from abc import ABC, abstractmethod
import logging
import os
from pathlib import Path
from typing import Any, Optional


class BaseExporter(ABC):
    """
    Abstract base class for data exporters.
    
    Provides common functionality for exporting data to files.
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the base exporter.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """
        Ensure output directory exists, create if it doesn't.
        """
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Output directory ensured: {self.output_dir}")
        except OSError as e:
            self.logger.error(f"Failed to create output directory: {e}")
            raise
    
    @abstractmethod
    def export(self, data: Any, filename: str, **kwargs) -> str:
        """
        Export data to file. Must be implemented by subclasses.
        
        Args:
            data: Data to export
            filename: Output filename
            **kwargs: Exporter-specific parameters
            
        Returns:
            Path to exported file
        """
        pass
    
    def _get_file_path(self, filename: str) -> Path:
        """
        Get full file path for output.
        
        Args:
            filename: Output filename
            
        Returns:
            Full path to output file
        """
        return self.output_dir / filename
