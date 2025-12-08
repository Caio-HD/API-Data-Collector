"""
Unit tests for GitHubParser
"""

import pytest
from src.parsers.github_parser import GitHubParser
from tests.conftest import (
    sample_repo_data,
    sample_issue_data,
    sample_pr_data,
    sample_profile_data
)


class TestGitHubParser:
    """Test cases for GitHubParser."""
    
    def test_init(self):
        """Test parser initialization."""
        parser = GitHubParser()
        assert parser is not None
    
    def test_parse_repos(self, sample_repo_data):
        """Test parsing repository data."""
        parser = GitHubParser()
        parsed = parser.parse([sample_repo_data], data_type='repos')
        
        assert len(parsed) == 1
        assert parsed[0]['name'] == 'test-repo'
        assert parsed[0]['stars'] == 42
        assert parsed[0]['forks'] == 10
        assert 'full_name' in parsed[0]
    
    def test_parse_issues(self, sample_issue_data):
        """Test parsing issue data."""
        parser = GitHubParser()
        parsed = parser.parse([sample_issue_data], data_type='issues')
        
        assert len(parsed) == 1
        assert parsed[0]['title'] == 'Test Issue'
        assert parsed[0]['state'] == 'open'
        assert parsed[0]['user'] == 'testuser'
        assert len(parsed[0]['labels']) == 2
    
    def test_parse_prs(self, sample_pr_data):
        """Test parsing pull request data."""
        parser = GitHubParser()
        parsed = parser.parse([sample_pr_data], data_type='prs')
        
        assert len(parsed) == 1
        assert parsed[0]['title'] == 'Test PR'
        assert parsed[0]['head_branch'] == 'feature-branch'
        assert parsed[0]['base_branch'] == 'main'
        assert parsed[0]['additions'] == 100
        assert parsed[0]['deletions'] == 50
    
    def test_parse_profile(self, sample_profile_data):
        """Test parsing profile data."""
        parser = GitHubParser()
        parsed = parser.parse(sample_profile_data, data_type='profile')
        
        assert parsed['login'] == 'testuser'
        assert parsed['name'] == 'Test User'
        assert parsed['public_repos'] == 10
        assert parsed['followers'] == 100
    
    def test_auto_detect_repos(self, sample_repo_data):
        """Test auto-detection of repository data."""
        parser = GitHubParser()
        parsed = parser.parse([sample_repo_data], data_type='auto')
        
        assert len(parsed) == 1
        assert 'name' in parsed[0]
    
    def test_parse_date(self):
        """Test date parsing."""
        parser = GitHubParser()
        date_str = "2023-01-01T00:00:00Z"
        parsed_date = parser._parse_date(date_str)
        
        assert parsed_date is not None
        assert '2023-01-01' in parsed_date
    
    def test_validate_repos(self, sample_repo_data):
        """Test validation of repository data."""
        parser = GitHubParser()
        parsed = parser.parse([sample_repo_data], data_type='repos')
        
        assert parser.validate(parsed) is True
        assert parser.validate(parsed, required_fields=['name', 'full_name']) is True
    
    def test_validate_invalid_data(self):
        """Test validation with invalid data."""
        parser = GitHubParser()
        
        assert parser.validate(None) is False
        assert parser.validate([]) is True
        assert parser.validate({}, required_fields=['missing_field']) is False
