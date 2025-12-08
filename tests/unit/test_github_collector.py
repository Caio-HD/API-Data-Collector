"""
Unit tests for GitHubCollector
"""

import pytest
from unittest.mock import Mock, patch
from src.collectors.github_collector import GitHubCollector


class TestGitHubCollector:
    """Test cases for GitHubCollector."""
    
    def test_init(self):
        """Test collector initialization."""
        collector = GitHubCollector(api_key="test_token")
        assert collector.base_url == "https://api.github.com"
        assert collector.api_key == "test_token"
        assert collector.rate_limit_delay == 0.5
    
    def test_set_auth(self):
        """Test authentication setup."""
        collector = GitHubCollector(api_key="test_token")
        assert collector.session.headers['Authorization'] == 'token test_token'
    
    @patch('src.collectors.github_collector.GitHubCollector._make_request')
    def test_collect_user_repos(self, mock_request):
        """Test collecting user repositories."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "repo1"},
            {"id": 2, "name": "repo2"}
        ]
        mock_request.return_value = mock_response
        
        collector = GitHubCollector()
        repos = collector.collect_user_repos("testuser")
        
        assert len(repos) == 2
        assert repos[0]["name"] == "repo1"
        mock_request.assert_called()
    
    @patch('src.collectors.github_collector.GitHubCollector._make_request')
    def test_collect_repo_issues(self, mock_request):
        """Test collecting repository issues."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "title": "Issue 1", "state": "open"}
        ]
        mock_request.return_value = mock_response
        
        collector = GitHubCollector()
        issues = collector.collect_repo_issues("owner", "repo")
        
        assert len(issues) == 1
        assert issues[0]["title"] == "Issue 1"
    
    @patch('src.collectors.github_collector.GitHubCollector._make_request')
    def test_collect_pull_requests(self, mock_request):
        """Test collecting pull requests."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "title": "PR 1", "state": "open"}
        ]
        mock_request.return_value = mock_response
        
        collector = GitHubCollector()
        prs = collector.collect_pull_requests("owner", "repo")
        
        assert len(prs) == 1
        assert prs[0]["title"] == "PR 1"
    
    @patch('src.collectors.github_collector.GitHubCollector._make_request')
    def test_collect_user_profile(self, mock_request):
        """Test collecting user profile."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "login": "testuser",
            "name": "Test User",
            "public_repos": 10
        }
        mock_request.return_value = mock_response
        
        collector = GitHubCollector()
        profile = collector.collect_user_profile("testuser")
        
        assert profile["login"] == "testuser"
        assert profile["public_repos"] == 10
    
    def test_collect_generic(self):
        """Test generic collect method routing."""
        collector = GitHubCollector()
        
        with patch.object(collector, 'collect_user_repos') as mock_repos:
            mock_repos.return_value = []
            collector.collect('repos', username='testuser')
            mock_repos.assert_called_once_with(username='testuser')
        
        with pytest.raises(ValueError):
            collector.collect('unknown_type')
