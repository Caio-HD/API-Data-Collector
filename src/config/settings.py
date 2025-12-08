"""
Application settings and configuration
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """
    Application settings loaded from environment variables.
    """
    
    def __init__(self):
        """Load settings from environment."""
        load_dotenv()
        
        self.github_token: Optional[str] = os.getenv('GITHUB_TOKEN')
        self.output_dir: str = os.getenv('OUTPUT_DIR', 'output')
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO')
        self.rate_limit_delay: float = float(os.getenv('RATE_LIMIT_DELAY', '0.5'))
        self.max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    
    def validate(self) -> bool:
        """
        Validate required settings.
        
        Returns:
            True if settings are valid
        """
        # GitHub token is optional but recommended
        return True
    
    def get_github_token(self) -> Optional[str]:
        """
        Get GitHub token if available.
        
        Returns:
            GitHub token or None
        """
        return self.github_token


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get settings singleton instance.
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.validate()
    return _settings
