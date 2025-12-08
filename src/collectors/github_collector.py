"""
GitHub API data collector
"""

import logging
from typing import Any, Dict, List, Optional
from ..core.base_collector import BaseCollector


class GitHubCollector(BaseCollector):
    """
    Collector for GitHub API data.
    
    Supports collecting:
    - User repositories
    - Repository issues
    - Pull requests
    - User profile information
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 0.5,
        max_retries: int = 3
    ):
        """
        Initialize GitHub collector.
        
        Args:
            api_key: GitHub personal access token
            rate_limit_delay: Delay between requests (GitHub allows 5000 req/hour with auth)
            max_retries: Maximum retry attempts
        """
        super().__init__(
            base_url="https://api.github.com",
            api_key=api_key,
            rate_limit_delay=rate_limit_delay,
            max_retries=max_retries
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _set_auth(self, api_key: str) -> None:
        """
        Set GitHub authentication using token.
        
        Args:
            api_key: GitHub personal access token
        """
        self.session.headers['Authorization'] = f'token {api_key}'
    
    def collect_user_repos(
        self,
        username: str,
        include_private: bool = False,
        per_page: int = 100,
        sort: str = 'updated',
        direction: str = 'desc'
    ) -> List[Dict[str, Any]]:
        """
        Collect repositories for a GitHub user.
        
        Args:
            username: GitHub username
            include_private: Include private repos (requires auth)
            per_page: Number of results per page (max 100)
            sort: Sort field (created, updated, pushed, full_name)
            direction: Sort direction (asc, desc)
            
        Returns:
            List of repository data dictionaries
        """
        self.logger.info(f"Collecting repositories for user: {username}")
        
        all_repos = []
        page = 1
        
        while True:
            params = {
                'per_page': min(per_page, 100),
                'page': page,
                'sort': sort,
                'direction': direction,
                'type': 'all' if include_private else 'public'
            }
            
            try:
                response = self._make_request(
                    f'/users/{username}/repos',
                    params=params
                )
                repos = response.json()
                
                if not repos:
                    break
                
                all_repos.extend(repos)
                self.logger.debug(f"Collected {len(repos)} repos from page {page}")
                
                # Check if there are more pages
                if len(repos) < per_page:
                    break
                
                page += 1
                
            except Exception as e:
                self._handle_errors(e)
                break
        
        self.logger.info(f"Total repositories collected: {len(all_repos)}")
        return all_repos
    
    def collect_repo_issues(
        self,
        owner: str,
        repo: str,
        state: str = 'all',
        per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Collect issues for a repository.
        
        Args:
            owner: Repository owner username
            repo: Repository name
            state: Issue state (open, closed, all)
            per_page: Number of results per page (max 100)
            
        Returns:
            List of issue data dictionaries
        """
        self.logger.info(f"Collecting issues for {owner}/{repo}")
        
        all_issues = []
        page = 1
        
        while True:
            params = {
                'state': state,
                'per_page': min(per_page, 100),
                'page': page
            }
            
            try:
                response = self._make_request(
                    f'/repos/{owner}/{repo}/issues',
                    params=params
                )
                issues = response.json()
                
                if not issues:
                    break
                
                all_issues.extend(issues)
                self.logger.debug(f"Collected {len(issues)} issues from page {page}")
                
                if len(issues) < per_page:
                    break
                
                page += 1
                
            except Exception as e:
                self._handle_errors(e)
                break
        
        self.logger.info(f"Total issues collected: {len(all_issues)}")
        return all_issues
    
    def collect_pull_requests(
        self,
        owner: str,
        repo: str,
        state: str = 'all',
        per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Collect pull requests for a repository.
        
        Args:
            owner: Repository owner username
            repo: Repository name
            state: PR state (open, closed, all)
            per_page: Number of results per page (max 100)
            
        Returns:
            List of pull request data dictionaries
        """
        self.logger.info(f"Collecting pull requests for {owner}/{repo}")
        
        all_prs = []
        page = 1
        
        while True:
            params = {
                'state': state,
                'per_page': min(per_page, 100),
                'page': page
            }
            
            try:
                response = self._make_request(
                    f'/repos/{owner}/{repo}/pulls',
                    params=params
                )
                prs = response.json()
                
                if not prs:
                    break
                
                all_prs.extend(prs)
                self.logger.debug(f"Collected {len(prs)} PRs from page {page}")
                
                if len(prs) < per_page:
                    break
                
                page += 1
                
            except Exception as e:
                self._handle_errors(e)
                break
        
        self.logger.info(f"Total pull requests collected: {len(all_prs)}")
        return all_prs
    
    def collect_user_profile(self, username: str) -> Dict[str, Any]:
        """
        Collect user profile information.
        
        Args:
            username: GitHub username
            
        Returns:
            User profile data dictionary
        """
        self.logger.info(f"Collecting profile for user: {username}")
        
        try:
            response = self._make_request(f'/users/{username}')
            profile = response.json()
            self.logger.info(f"Profile collected for {username}")
            return profile
        except Exception as e:
            self._handle_errors(e)
            return {}
    
    def collect(self, collection_type: str, **kwargs) -> Any:
        """
        Generic collect method that routes to specific collection methods.
        
        Args:
            collection_type: Type of collection (repos, issues, prs, profile)
            **kwargs: Parameters for specific collection method
            
        Returns:
            Collected data
        """
        collection_methods = {
            'repos': self.collect_user_repos,
            'issues': self.collect_repo_issues,
            'prs': self.collect_pull_requests,
            'profile': self.collect_user_profile
        }
        
        method = collection_methods.get(collection_type)
        if not method:
            raise ValueError(f"Unknown collection type: {collection_type}")
        
        return method(**kwargs)
