"""
GitHub Trending Scraper
"""

import logging
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from ..core.base_collector import BaseCollector


class GitHubScraper(BaseCollector):
    """
    Scraper for GitHub Trending data.
    
    Collects:
    - Trending repositories by language
    """
    
    def __init__(
        self, 
        rate_limit_delay: float = 1.0, 
        max_retries: int = 3
    ):
        """
        Initialize GitHub scraper.
        
        Args:
            rate_limit_delay: Delay between requests
            max_retries: Maximum retry attempts
        """
        super().__init__(
            base_url="https://github.com",
            api_key=None,  # No API key needed for scraping
            rate_limit_delay=rate_limit_delay,
            max_retries=max_retries
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ua = UserAgent()
    
    def collect_trending(
        self,
        language: str = '',
        since: str = 'daily'
    ) -> List[Dict[str, Any]]:
        """
        Collect trending repositories.
        
        Args:
            language: Programming language (e.g., 'python', 'javascript')
            since: Time range ('daily', 'weekly', 'monthly')
            
        Returns:
            List of trending repository dictionaries
        """
        self.logger.info(f"Collecting trending repos for language: '{language}' since: '{since}'")
        
        params = {}
        if since != 'daily':
            params['since'] = since
            
        url_path = 'trending'
        if language:
            url_path = f'trending/{language}'
            
        # Randomize User-Agent to avoid blocking
        headers = {'User-Agent': self.ua.random}
        
        try:
            response = self._make_request(
                url_path,
                params=params,
                headers=headers
            )
            
            return self._parse_trending_page(response.text)
            
        except Exception as e:
            self._handle_errors(e)
            return []
    
    def _parse_trending_page(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Parse GitHub trending HTML page.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            List of parsed repository data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        repos = []
        
        # GitHub trending structure changes often, but generally uses <article> or .Box-row
        repo_rows = soup.select('article.Box-row')
        
        for row in repo_rows:
            try:
                # Name and User
                title_h1 = row.select_one('h2.h3 a')
                if not title_h1:
                    continue
                    
                full_name = title_h1.get('href', '').strip('/')
                parts = full_name.split('/')
                owner = parts[0] if len(parts) > 0 else ''
                name = parts[1] if len(parts) > 1 else ''
                
                # Description
                desc_p = row.select_one('p.col-9')
                description = desc_p.text.strip() if desc_p else ''
                
                # Stats (Stars, Forks)
                stats_div = row.select_one('div.f6')
                language_span = stats_div.select_one('span[itemprop="programmingLanguage"]')
                language = language_span.text.strip() if language_span else 'Unknown'
                
                # Stars are usually the first link in the stats div
                stars_link = stats_div.select_one('a[href$="/stargazers"]')
                stars_text = stars_link.text.strip().replace(',', '') if stars_link else '0'
                try:
                    stars = int(stars_text)
                except ValueError:
                    stars = 0
                
                # Fork count
                forks_link = stats_div.select_one('a[href$="/forks"]')
                forks_text = forks_link.text.strip().replace(',', '') if forks_link else '0'
                try:
                    forks = int(forks_text)
                except ValueError:
                    forks = 0
                
                # Stars today/this week/month
                stars_today_span = stats_div.select_one('span.d-inline-block.float-sm-right')
                stars_today_text = stars_today_span.text.strip().split()[0].replace(',', '') if stars_today_span else '0'
                try:
                    stars_since = int(stars_today_text)
                except ValueError:
                    stars_since = 0

                repos.append({
                    'full_name': full_name,
                    'owner': owner,
                    'name': name,
                    'description': description,
                    'language': language,
                    'stars_total': stars,
                    'forks_total': forks,
                    'stars_since': stars_since,
                    'url': f"https://github.com/{full_name}"
                })
                
            except Exception as e:
                self.logger.warning(f"Error parsing a trending row: {e}")
                continue
                
        self.logger.info(f"Parsed {len(repos)} trending repositories")
        return repos

    def collect(self, collection_type: str, **kwargs) -> Any:
        """
        Implementation of abstract collect method.
        """
        if collection_type == 'trending':
            return self.collect_trending(**kwargs)
        raise ValueError(f"Unknown collection type: {collection_type}")
