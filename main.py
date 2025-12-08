"""
Main script for API Data Collector
"""

import argparse
import sys
from src.collectors.github_collector import GitHubCollector
from src.collectors.github_scraper import GitHubScraper
from src.parsers.github_parser import GitHubParser
from src.exporters.json_exporter import JSONExporter
from src.exporters.csv_exporter import CSVExporter
from src.config import get_settings
from src.utils.logger import setup_logger


def collect_repos(username: str, export_format: str = 'json'):
    """
    Collect and export user repositories.
    
    Args:
        username: GitHub username
        export_format: Export format (json or csv)
    """
    settings = get_settings()
    logger = setup_logger(level=settings.log_level)
    
    logger.info(f"Starting repository collection for user: {username}")
    
    # Initialize components
    collector = GitHubCollector(api_key=settings.github_token)
    parser = GitHubParser()
    
    # Collect data
    try:
        raw_data = collector.collect_user_repos(username)
        logger.info(f"Collected {len(raw_data)} repositories")
        
        # Parse data
        parsed_data = parser.parse(raw_data, data_type='repos')
        logger.info(f"Parsed {len(parsed_data)} repositories")
        
        # Export data
        if export_format.lower() == 'csv':
            exporter = CSVExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{username}_repos.csv")
        else:
            exporter = JSONExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{username}_repos.json")
        
        logger.info(f"Data exported to: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error collecting repositories: {e}")
        sys.exit(1)


def collect_issues(owner: str, repo: str, export_format: str = 'json'):
    """
    Collect and export repository issues.
    
    Args:
        owner: Repository owner
        repo: Repository name
        export_format: Export format (json or csv)
    """
    settings = get_settings()
    logger = setup_logger(level=settings.log_level)
    
    logger.info(f"Starting issue collection for {owner}/{repo}")
    
    # Initialize components
    collector = GitHubCollector(api_key=settings.github_token)
    parser = GitHubParser()
    
    # Collect data
    try:
        raw_data = collector.collect_repo_issues(owner, repo)
        logger.info(f"Collected {len(raw_data)} issues")
        
        # Parse data
        parsed_data = parser.parse(raw_data, data_type='issues')
        logger.info(f"Parsed {len(parsed_data)} issues")
        
        # Export data
        filename = f"{owner}_{repo}_issues"
        if export_format.lower() == 'csv':
            exporter = CSVExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{filename}.csv")
        else:
            exporter = JSONExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{filename}.json")
        
        logger.info(f"Data exported to: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error collecting issues: {e}")
        sys.exit(1)


def collect_prs(owner: str, repo: str, export_format: str = 'json'):
    """
    Collect and export pull requests.
    
    Args:
        owner: Repository owner
        repo: Repository name
        export_format: Export format (json or csv)
    """
    settings = get_settings()
    logger = setup_logger(level=settings.log_level)
    
    logger.info(f"Starting PR collection for {owner}/{repo}")
    
    # Initialize components
    collector = GitHubCollector(api_key=settings.github_token)
    parser = GitHubParser()
    
    # Collect data
    try:
        raw_data = collector.collect_pull_requests(owner, repo)
        logger.info(f"Collected {len(raw_data)} pull requests")
        
        # Parse data
        parsed_data = parser.parse(raw_data, data_type='prs')
        logger.info(f"Parsed {len(parsed_data)} pull requests")
        
        # Export data
        filename = f"{owner}_{repo}_prs"
        if export_format.lower() == 'csv':
            exporter = CSVExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{filename}.csv")
        else:
            exporter = JSONExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{filename}.json")
        
        logger.info(f"Data exported to: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error collecting pull requests: {e}")
        sys.exit(1)


def collect_profile(username: str, export_format: str = 'json'):
    """
    Collect and export user profile.
    
    Args:
        username: GitHub username
        export_format: Export format (json or csv)
    """
    settings = get_settings()
    logger = setup_logger(level=settings.log_level)
    
    logger.info(f"Starting profile collection for user: {username}")
    
    # Initialize components
    collector = GitHubCollector(api_key=settings.github_token)
    parser = GitHubParser()
    
    # Collect data
    try:
        raw_data = collector.collect_user_profile(username)
        logger.info("Profile collected")
        
        # Parse data
        parsed_data = parser.parse(raw_data, data_type='profile')
        logger.info("Profile parsed")
        
        # Export data
        if export_format.lower() == 'csv':
            exporter = CSVExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{username}_profile.csv")
        else:
            exporter = JSONExporter(output_dir=settings.output_dir)
            file_path = exporter.export(parsed_data, f"{username}_profile.json")
        
        logger.info(f"Data exported to: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error collecting profile: {e}")
        sys.exit(1)


def collect_trending(language: str = '', since: str = 'daily', export_format: str = 'json'):
    """
    Collect and export trending repositories.
    
    Args:
        language: Programming language
        since: Time range (daily, weekly, monthly)
        export_format: Export format (json or csv)
    """
    settings = get_settings()
    logger = setup_logger(level=settings.log_level)
    
    logger.info(f"Starting trending collection for {language if language else 'all languages'} ({since})")
    
    # Initialize components
    scraper = GitHubScraper()
    
    # Collect data
    try:
        data = scraper.collect_trending(language, since)
        logger.info(f"Collected {len(data)} trending repositories")
        
        # Export data
        filename = f"trending_{language if language else 'all'}_{since}"
        if export_format.lower() == 'csv':
            exporter = CSVExporter(output_dir=settings.output_dir)
            file_path = exporter.export(data, f"{filename}.csv")
        else:
            exporter = JSONExporter(output_dir=settings.output_dir)
            file_path = exporter.export(data, f"{filename}.json")
        
        logger.info(f"Data exported to: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error collecting trending repos: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='API Data Collector - Collect data from GitHub API'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Repos command
    repos_parser = subparsers.add_parser('repos', help='Collect user repositories')
    repos_parser.add_argument('username', help='GitHub username')
    repos_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                             help='Export format (default: json)')
    
    # Issues command
    issues_parser = subparsers.add_parser('issues', help='Collect repository issues')
    issues_parser.add_argument('owner', help='Repository owner')
    issues_parser.add_argument('repo', help='Repository name')
    issues_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                              help='Export format (default: json)')
    
    # PRs command
    prs_parser = subparsers.add_parser('prs', help='Collect pull requests')
    prs_parser.add_argument('owner', help='Repository owner')
    prs_parser.add_argument('repo', help='Repository name')
    prs_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                           help='Export format (default: json)')
    
    # Profile command
    profile_parser = subparsers.add_parser('profile', help='Collect user profile')
    profile_parser.add_argument('username', help='GitHub username')
    profile_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                               help='Export format (default: json)')
    
    # Trending command
    trending_parser = subparsers.add_parser('trending', help='Collect trending repositories')
    trending_parser.add_argument('--language', default='', help='Programming language')
    trending_parser.add_argument('--since', choices=['daily', 'weekly', 'monthly'], default='daily',
                                help='Time range (default: daily)')
    trending_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                                help='Export format (default: json)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to appropriate function
    if args.command == 'repos':
        collect_repos(args.username, args.format)
    elif args.command == 'issues':
        collect_issues(args.owner, args.repo, args.format)
    elif args.command == 'prs':
        collect_prs(args.owner, args.repo, args.format)
    elif args.command == 'profile':
        collect_profile(args.username, args.format)
    elif args.command == 'trending':
        collect_trending(args.language, args.since, args.format)


if __name__ == '__main__':
    main()
