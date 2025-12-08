"""
Base collector class for data collection
"""

from abc import ABC, abstractmethod
import time
import logging
from typing import Any, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseCollector(ABC):
    """
    Abstract base class for data collectors.
    
    Provides common functionality for making HTTP requests,
    handling errors, and managing rate limiting.
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 1.0,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize the base collector.
        
        Args:
            base_url: Base URL for API requests
            api_key: Optional API key for authentication
            rate_limit_delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'API-Data-Collector/1.0',
            'Accept': 'application/json'
        })
        
        if api_key:
            self._set_auth(api_key)
    
    def _set_auth(self, api_key: str) -> None:
        """
        Set authentication headers. Override in subclasses if needed.
        
        Args:
            api_key: API key for authentication
        """
        self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def _make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with error handling and rate limiting.
        
        Args:
            endpoint: API endpoint (relative to base_url)
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If request fails after retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Apply rate limiting
        self._rate_limit()
        
        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        try:
            self.logger.debug(f"Making {method} request to {url}")
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=request_headers,
                timeout=self.timeout,
                **kwargs
            )
            
            # Handle response
            self._handle_response(response)
            
            return response
            
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def _handle_response(self, response: requests.Response) -> None:
        """
        Handle HTTP response and raise appropriate errors.
        
        Args:
            response: Response object
            
        Raises:
            requests.HTTPError: For HTTP error status codes
        """
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            self.logger.warning(f"Rate limit exceeded. Waiting {retry_after} seconds")
            time.sleep(retry_after)
            raise requests.HTTPError(f"Rate limit exceeded: {response.status_code}")
        
        response.raise_for_status()
    
    def _rate_limit(self) -> None:
        """
        Apply rate limiting delay between requests.
        """
        if self.rate_limit_delay > 0:
            time.sleep(self.rate_limit_delay)
    
    def _handle_errors(self, error: Exception) -> None:
        """
        Handle and log errors.
        
        Args:
            error: Exception to handle
        """
        self.logger.error(f"Error occurred: {error}", exc_info=True)
    
    @abstractmethod
    def collect(self, **kwargs) -> Any:
        """
        Collect data from the source. Must be implemented by subclasses.
        
        Args:
            **kwargs: Collector-specific parameters
            
        Returns:
            Collected data
        """
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()
