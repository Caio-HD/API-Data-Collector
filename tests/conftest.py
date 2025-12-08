"""
Pytest configuration and shared fixtures
"""

import pytest
import json
from pathlib import Path


@pytest.fixture
def sample_repo_data():
    """Sample repository data from GitHub API."""
    return {
        "id": 123456,
        "name": "test-repo",
        "full_name": "testuser/test-repo",
        "description": "A test repository",
        "html_url": "https://github.com/testuser/test-repo",
        "clone_url": "https://github.com/testuser/test-repo.git",
        "language": "Python",
        "stargazers_count": 42,
        "forks_count": 10,
        "watchers_count": 5,
        "open_issues_count": 3,
        "private": False,
        "fork": False,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-12-01T00:00:00Z",
        "pushed_at": "2023-12-01T00:00:00Z",
        "default_branch": "main",
        "topics": ["python", "testing"]
    }


@pytest.fixture
def sample_issue_data():
    """Sample issue data from GitHub API."""
    return {
        "id": 789012,
        "number": 1,
        "title": "Test Issue",
        "body": "This is a test issue",
        "state": "open",
        "html_url": "https://github.com/testuser/test-repo/issues/1",
        "user": {"login": "testuser"},
        "labels": [{"name": "bug"}, {"name": "enhancement"}],
        "assignees": [{"login": "assignee1"}],
        "comments": 2,
        "created_at": "2023-11-01T00:00:00Z",
        "updated_at": "2023-11-02T00:00:00Z",
        "closed_at": None
    }


@pytest.fixture
def sample_pr_data():
    """Sample pull request data from GitHub API."""
    return {
        "id": 345678,
        "number": 5,
        "title": "Test PR",
        "body": "This is a test pull request",
        "state": "open",
        "html_url": "https://github.com/testuser/test-repo/pull/5",
        "user": {"login": "contributor"},
        "head": {"ref": "feature-branch"},
        "base": {"ref": "main"},
        "labels": [{"name": "feature"}],
        "assignees": [],
        "requested_reviewers": [{"login": "reviewer1"}],
        "comments": 1,
        "review_comments": 2,
        "commits": 3,
        "additions": 100,
        "deletions": 50,
        "changed_files": 5,
        "merged": False,
        "mergeable": True,
        "created_at": "2023-11-15T00:00:00Z",
        "updated_at": "2023-11-16T00:00:00Z",
        "closed_at": None,
        "merged_at": None
    }


@pytest.fixture
def sample_profile_data():
    """Sample user profile data from GitHub API."""
    return {
        "id": 111222,
        "login": "testuser",
        "name": "Test User",
        "bio": "A test user",
        "company": "Test Company",
        "blog": "https://testuser.com",
        "location": "Test City",
        "email": "test@example.com",
        "hireable": True,
        "public_repos": 10,
        "public_gists": 5,
        "followers": 100,
        "following": 50,
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2023-12-01T00:00:00Z",
        "html_url": "https://github.com/testuser"
    }


@pytest.fixture
def mock_response(monkeypatch):
    """Mock requests.Response object."""
    class MockResponse:
        def __init__(self, json_data, status_code=200, headers=None):
            self.json_data = json_data
            self.status_code = status_code
            self.headers = headers or {}
            self.text = json.dumps(json_data) if json_data else ""
        
        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP {self.status_code}")
    
    return MockResponse


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for tests."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return str(output_dir)
