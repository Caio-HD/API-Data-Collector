"""
Base parser class for data parsing
"""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional


class BaseParser(ABC):
    """
    Abstract base class for data parsers.
    
    Provides common functionality for parsing and validating data.
    """
    
    def __init__(self):
        """Initialize the base parser."""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def parse(self, data: Any, **kwargs) -> Any:
        """
        Parse raw data into structured format. Must be implemented by subclasses.
        
        Args:
            data: Raw data to parse
            **kwargs: Parser-specific parameters
            
        Returns:
            Parsed data
        """
        pass
    
    def validate(self, data: Any, required_fields: Optional[List[str]] = None) -> bool:
        """
        Validate parsed data structure.
        
        Args:
            data: Data to validate
            required_fields: List of required field names
            
        Returns:
            True if data is valid, False otherwise
        """
        if data is None:
            self.logger.warning("Data is None")
            return False
        
        if required_fields:
            if isinstance(data, dict):
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.logger.warning(f"Missing required fields: {missing_fields}")
                    return False
            elif isinstance(data, list):
                if len(data) == 0:
                    self.logger.warning("Data list is empty")
                    # Empty list is valid structure (just no results)
                    return True
                # Validate first item if list
                if isinstance(data[0], dict):
                    missing_fields = [
                        field for field in required_fields
                        if field not in data[0]
                    ]
                    if missing_fields:
                        self.logger.warning(f"Missing required fields in list items: {missing_fields}")
                        return False
        
        return True
    
    def normalize(self, data: Any) -> Any:
        """
        Normalize data format. Override in subclasses for specific normalization.
        
        Args:
            data: Data to normalize
            
        Returns:
            Normalized data
        """
        return data
