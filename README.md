# API Data Collector

## 📋 About

API Data Collector is a Python-based tool designed to automate data collection from the GitHub API. The project demonstrates skills in API integration, data parsing, automated data extraction workflows, and modular software architecture.

This tool solves the problem of manual data collection by providing a flexible, extensible framework for gathering data from GitHub (repositories, issues, pull requests, and user profiles), parsing it into structured formats, and exporting it for further analysis or processing.

## 🚀 Technologies

- **Language**: Python 3.8+
- **HTTP Requests**: Requests library
- **Testing**: PyTest
- **Data Processing**: JSON, CSV handling
- **Configuration**: python-dotenv

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- GitHub Personal Access Token (optional but recommended for higher rate limits)

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd api-data-collector
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your GitHub token and configuration
```

To get a GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with appropriate scopes (at minimum `public_repo` for public repositories)
3. Copy the token and add it to your `.env` file

## 💻 Usage

### Command Line Interface

The tool provides a simple CLI for common operations:

#### Collect User Repositories

```bash
# Collect repositories in JSON format (default)
python main.py repos octocat

# Collect repositories in CSV format
python main.py repos octocat --format csv
```

#### Collect Repository Issues

```bash
# Collect all issues from a repository
python main.py issues owner repo-name

# Export as CSV
python main.py issues owner repo-name --format csv
```

#### Collect Pull Requests

```bash
# Collect all pull requests
python main.py prs owner repo-name

# Export as CSV
python main.py prs owner repo-name --format csv
```

#### Collect User Profile

```bash
# Collect user profile information
python main.py profile username

# Export as CSV
python main.py profile username --format csv
```

### Using Python API

#### Basic Example - Collect Repositories

```python
from src.collectors.github_collector import GitHubCollector
from src.parsers.github_parser import GitHubParser
from src.exporters.json_exporter import JSONExporter

# Initialize collector (token is optional but recommended)
collector = GitHubCollector(api_key="your_github_token")

# Collect repositories
repos = collector.collect_user_repos("octocat")

# Parse the data
parser = GitHubParser()
parsed_repos = parser.parse(repos, data_type='repos')

# Export to JSON
exporter = JSONExporter(output_dir="output")
file_path = exporter.export(parsed_repos, "octocat_repos.json")

print(f"Exported {len(parsed_repos)} repositories to {file_path}")
```

#### Collect and Parse Issues

```python
from src.collectors.github_collector import GitHubCollector
from src.parsers.github_parser import GitHubParser
from src.exporters.csv_exporter import CSVExporter

collector = GitHubCollector(api_key="your_github_token")
parser = GitHubParser()
exporter = CSVExporter(output_dir="output")

# Collect issues
issues = collector.collect_repo_issues("owner", "repo-name", state="open")

# Parse issues (filters out pull requests automatically)
parsed_issues = parser.parse(issues, data_type='issues')

# Export to CSV
file_path = exporter.export(parsed_issues, "repo_issues.csv")
```

#### Collect Pull Requests with Details

```python
from src.collectors.github_collector import GitHubCollector
from src.parsers.github_parser import GitHubParser

collector = GitHubCollector(api_key="your_github_token")
parser = GitHubParser()

# Collect pull requests
prs = collector.collect_pull_requests("owner", "repo-name", state="all")

# Parse PR data
parsed_prs = parser.parse(prs, data_type='prs')

# Access parsed data
for pr in parsed_prs:
    print(f"PR #{pr['number']}: {pr['title']}")
    print(f"  Additions: {pr['additions']}, Deletions: {pr['deletions']}")
    print(f"  Status: {'Merged' if pr['merged'] else pr['state']}")
```

#### Complete Pipeline Example

```python
from src.collectors.github_collector import GitHubCollector
from src.parsers.github_parser import GitHubParser
from src.exporters.json_exporter import JSONExporter
from src.config import get_settings
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger(level='INFO')

# Get settings
settings = get_settings()

# Initialize components
collector = GitHubCollector(api_key=settings.github_token)
parser = GitHubParser()
exporter = JSONExporter(output_dir=settings.output_dir)

# Collect multiple data types
username = "octocat"

# Repositories
repos = collector.collect_user_repos(username)
parsed_repos = parser.parse(repos, data_type='repos')
exporter.export(parsed_repos, f"{username}_repos.json")

# Profile
profile = collector.collect_user_profile(username)
parsed_profile = parser.parse(profile, data_type='profile')
exporter.export(parsed_profile, f"{username}_profile.json")

logger.info("Collection complete!")
```

### Advanced Usage

#### Custom Rate Limiting

```python
# Adjust rate limiting for different API limits
collector = GitHubCollector(
    api_key="your_token",
    rate_limit_delay=0.5  # 0.5 seconds between requests
)
```

#### Export Multiple Datasets

```python
from src.exporters.json_exporter import JSONExporter

exporter = JSONExporter()

# Export multiple datasets at once
data_dict = {
    "repos": parsed_repos,
    "issues": parsed_issues,
    "prs": parsed_prs
}

files = exporter.export_multiple(data_dict, prefix="github_")
```

## 🏗️ Project Structure

```
api-data-collector/
├── src/
│   ├── core/                 # Base classes
│   │   ├── base_collector.py
│   │   ├── base_parser.py
│   │   └── base_exporter.py
│   ├── collectors/            # Data collection modules
│   │   └── github_collector.py
│   ├── parsers/              # Data parsing utilities
│   │   └── github_parser.py
│   ├── exporters/            # Data export modules
│   │   ├── json_exporter.py
│   │   └── csv_exporter.py
│   ├── config/               # Configuration
│   │   └── settings.py
│   └── utils/               # Utilities
│       └── logger.py
├── tests/                    # Test files
│   ├── unit/
│   │   ├── test_github_collector.py
│   │   ├── test_github_parser.py
│   │   └── test_exporters.py
│   └── fixtures/
│       └── github_responses.py
├── output/                   # Output directory for collected data
├── main.py                   # CLI entry point
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### Key Components

- **BaseCollector**: Abstract base class providing HTTP request handling, rate limiting, and error management
- **GitHubCollector**: Implementation for GitHub API with methods for repositories, issues, PRs, and profiles
- **BaseParser**: Abstract base class for data parsing and validation
- **GitHubParser**: Normalizes and structures GitHub API responses
- **BaseExporter**: Abstract base class for data export
- **JSONExporter**: Exports data to JSON format with formatting options
- **CSVExporter**: Exports data to CSV with automatic flattening of nested structures

## 🧪 Running Tests

Execute unit tests to verify functionality:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_github_collector.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📝 Configuration

Configuration is managed through environment variables. See `.env.example` for available options:

- `GITHUB_TOKEN`: Your GitHub Personal Access Token (recommended)
- `OUTPUT_DIR`: Directory for output files (default: `output`)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `RATE_LIMIT_DELAY`: Delay between requests in seconds (default: 0.5)
- `MAX_RETRIES`: Maximum retry attempts for failed requests (default: 3)

## 🔧 Rate Limiting

GitHub API has rate limits:
- **Unauthenticated**: 60 requests per hour
- **Authenticated**: 5,000 requests per hour

The collector automatically handles rate limiting and will wait when limits are exceeded. Using a GitHub token is highly recommended for production use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
