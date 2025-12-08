"""
Sample GitHub API responses for testing
"""

# Sample repository response
SAMPLE_REPO = {
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

# Sample issue response
SAMPLE_ISSUE = {
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

# Sample pull request response
SAMPLE_PR = {
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

# Sample user profile response
SAMPLE_PROFILE = {
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
