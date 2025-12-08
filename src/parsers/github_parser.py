"""
GitHub API data parser
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from ..core.base_parser import BaseParser


class GitHubParser(BaseParser):
    """
    Parser for GitHub API data.
    
    Normalizes and structures GitHub API responses.
    """
    
    def __init__(self):
        """Initialize GitHub parser."""
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def parse(self, data: Any, data_type: str = 'auto', **kwargs) -> Any:
        """
        Parse GitHub API data.
        
        Args:
            data: Raw data from GitHub API
            data_type: Type of data (repos, issues, prs, profile, auto)
            **kwargs: Additional parsing options
            
        Returns:
            Parsed data
        """
        if data_type == 'auto':
            data_type = self._detect_data_type(data)
        
        parsers = {
            'repos': self._parse_repos,
            'issues': self._parse_issues,
            'prs': self._parse_pull_requests,
            'profile': self._parse_profile
        }
        
        parser = parsers.get(data_type)
        if not parser:
            self.logger.warning(f"Unknown data type: {data_type}, returning raw data")
            return data
        
        return parser(data, **kwargs)
    
    def _detect_data_type(self, data: Any) -> str:
        """
        Auto-detect data type from structure.
        
        Args:
            data: Data to analyze
            
        Returns:
            Detected data type
        """
        if not data:
            return 'unknown'
        
        if isinstance(data, list) and len(data) > 0:
            sample = data[0]
            if isinstance(sample, dict):
                if 'pull_request' in sample:
                    return 'issues'
                elif 'merged_at' in sample or 'mergeable' in sample:
                    return 'prs'
                elif 'full_name' in sample or 'clone_url' in sample:
                    return 'repos'
        elif isinstance(data, dict):
            if 'login' in data and 'public_repos' in data:
                return 'profile'
            elif 'full_name' in data or 'clone_url' in data:
                return 'repos'
        
        return 'unknown'
    
    def _parse_repos(self, repos: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        Parse repository data.
        
        Args:
            repos: List of repository dictionaries
            
        Returns:
            Parsed repository data
        """
        if not isinstance(repos, list):
            repos = [repos] if repos else []
        
        parsed = []
        for repo in repos:
            parsed_repo = {
                'id': repo.get('id'),
                'name': repo.get('name'),
                'full_name': repo.get('full_name'),
                'description': repo.get('description', ''),
                'url': repo.get('html_url'),
                'clone_url': repo.get('clone_url'),
                'language': repo.get('language'),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'watchers': repo.get('watchers_count', 0),
                'open_issues': repo.get('open_issues_count', 0),
                'is_private': repo.get('private', False),
                'is_fork': repo.get('fork', False),
                'created_at': self._parse_date(repo.get('created_at')),
                'updated_at': self._parse_date(repo.get('updated_at')),
                'pushed_at': self._parse_date(repo.get('pushed_at')),
                'default_branch': repo.get('default_branch', 'main'),
                'topics': repo.get('topics', [])
            }
            parsed.append(parsed_repo)
        
        return parsed
    
    def _parse_issues(self, issues: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        Parse issue data.
        
        Args:
            issues: List of issue dictionaries
            
        Returns:
            Parsed issue data
        """
        if not isinstance(issues, list):
            issues = [issues] if issues else []
        
        parsed = []
        for issue in issues:
            # Skip pull requests (they appear in issues endpoint)
            if issue.get('pull_request'):
                continue
            
            parsed_issue = {
                'id': issue.get('id'),
                'number': issue.get('number'),
                'title': issue.get('title'),
                'body': issue.get('body', ''),
                'state': issue.get('state'),
                'url': issue.get('html_url'),
                'user': issue.get('user', {}).get('login') if issue.get('user') else None,
                'labels': [label.get('name') for label in issue.get('labels', [])],
                'assignees': [assignee.get('login') for assignee in issue.get('assignees', [])],
                'comments': issue.get('comments', 0),
                'created_at': self._parse_date(issue.get('created_at')),
                'updated_at': self._parse_date(issue.get('updated_at')),
                'closed_at': self._parse_date(issue.get('closed_at'))
            }
            parsed.append(parsed_issue)
        
        return parsed
    
    def _parse_pull_requests(self, prs: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        Parse pull request data.
        
        Args:
            prs: List of pull request dictionaries
            
        Returns:
            Parsed pull request data
        """
        if not isinstance(prs, list):
            prs = [prs] if prs else []
        
        parsed = []
        for pr in prs:
            parsed_pr = {
                'id': pr.get('id'),
                'number': pr.get('number'),
                'title': pr.get('title'),
                'body': pr.get('body', ''),
                'state': pr.get('state'),
                'url': pr.get('html_url'),
                'user': pr.get('user', {}).get('login') if pr.get('user') else None,
                'head_branch': pr.get('head', {}).get('ref') if pr.get('head') else None,
                'base_branch': pr.get('base', {}).get('ref') if pr.get('base') else None,
                'labels': [label.get('name') for label in pr.get('labels', [])],
                'assignees': [assignee.get('login') for assignee in pr.get('assignees', [])],
                'reviewers': [reviewer.get('login') for reviewer in pr.get('requested_reviewers', [])],
                'comments': pr.get('comments', 0),
                'review_comments': pr.get('review_comments', 0),
                'commits': pr.get('commits', 0),
                'additions': pr.get('additions'),
                'deletions': pr.get('deletions'),
                'changed_files': pr.get('changed_files'),
                'merged': pr.get('merged', False),
                'mergeable': pr.get('mergeable'),
                'created_at': self._parse_date(pr.get('created_at')),
                'updated_at': self._parse_date(pr.get('updated_at')),
                'closed_at': self._parse_date(pr.get('closed_at')),
                'merged_at': self._parse_date(pr.get('merged_at'))
            }
            parsed.append(parsed_pr)
        
        return parsed
    
    def _parse_profile(self, profile: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Parse user profile data.
        
        Args:
            profile: User profile dictionary
            
        Returns:
            Parsed profile data
        """
        if not isinstance(profile, dict):
            return {}
        
        parsed = {
            'id': profile.get('id'),
            'login': profile.get('login'),
            'name': profile.get('name'),
            'bio': profile.get('bio', ''),
            'company': profile.get('company'),
            'blog': profile.get('blog'),
            'location': profile.get('location'),
            'email': profile.get('email'),
            'hireable': profile.get('hireable'),
            'public_repos': profile.get('public_repos', 0),
            'public_gists': profile.get('public_gists', 0),
            'followers': profile.get('followers', 0),
            'following': profile.get('following', 0),
            'created_at': self._parse_date(profile.get('created_at')),
            'updated_at': self._parse_date(profile.get('updated_at')),
            'url': profile.get('html_url')
        }
        
        return parsed
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """
        Parse and normalize date string.
        
        Args:
            date_str: ISO format date string
            
        Returns:
            Normalized date string or None
        """
        if not date_str:
            return None
        
        try:
            # GitHub uses ISO 8601 format
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.isoformat()
        except (ValueError, AttributeError):
            self.logger.warning(f"Failed to parse date: {date_str}")
            return date_str
    
    def validate(self, data: Any, required_fields: Optional[List[str]] = None) -> bool:
        """
        Validate parsed GitHub data.
        
        Args:
            data: Data to validate
            required_fields: Required fields (optional)
            
        Returns:
            True if valid, False otherwise
        """
        if not super().validate(data, required_fields):
            return False
        
        # Additional GitHub-specific validation
        if isinstance(data, list) and len(data) > 0:
            # Validate first item has expected structure
            first_item = data[0]
            if not isinstance(first_item, dict):
                self.logger.warning("List items should be dictionaries")
                return False
        
        return True
