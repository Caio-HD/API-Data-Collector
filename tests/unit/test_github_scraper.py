"""
Unit tests for GitHubScraper
"""

import pytest
from unittest.mock import Mock, patch
from src.collectors.github_scraper import GitHubScraper


class TestGitHubScraper:
    """Test cases for GitHubScraper."""
    
    def test_init(self):
        """Test scraper initialization."""
        scraper = GitHubScraper()
        assert scraper.base_url == "https://github.com"
        assert scraper.api_key is None
    
    @patch('src.collectors.github_scraper.GitHubScraper._make_request')
    def test_collect_trending(self, mock_request):
        """Test collecting trending repos."""
        mock_response = Mock()
        mock_response.text = """
        <html>
            <article class="Box-row">
                <h2 class="h3 applied-text-shadow-small">
                    <a href="/owner/repo">owner/repo</a>
                </h2>
                <p class="col-9">Description</p>
                <div class="f6">
                    <span itemprop="programmingLanguage">Python</span>
                    <a href="/owner/repo/stargazers">1,000</a>
                    <a href="/owner/repo/forks">100</a>
                    <span class="d-inline-block float-sm-right">50 stars today</span>
                </div>
            </article>
        </html>
        """
        mock_request.return_value = mock_response
        
        scraper = GitHubScraper()
        repos = scraper.collect_trending(language="python")
        
        assert len(repos) == 1
        repo = repos[0]
        assert repo["full_name"] == "owner/repo"
        assert repo["owner"] == "owner"
        assert repo["name"] == "repo"
        assert repo["description"] == "Description"
        assert repo["language"] == "Python"
        assert repo["stars_total"] == 1000
        assert repo["forks_total"] == 100
        assert repo["stars_since"] == 50
    
    @patch('src.collectors.github_scraper.GitHubScraper._make_request')
    def test_collect_trending_parsing_error(self, mock_request):
        """Test collecting trending repos with malformed HTML."""
        mock_response = Mock()
        mock_response.text = "<html>Invalid HTML</html>"
        mock_request.return_value = mock_response
        
        scraper = GitHubScraper()
        repos = scraper.collect_trending()
        
        assert len(repos) == 0
    
    def test_collect_generic(self):
        """Test generic collect method."""
        scraper = GitHubScraper()
        
        with patch.object(scraper, 'collect_trending') as mock_trending:
            mock_trending.return_value = []
            scraper.collect('trending', language='python')
            mock_trending.assert_called_once_with(language='python')
        
        with pytest.raises(ValueError):
            scraper.collect('unknown')
