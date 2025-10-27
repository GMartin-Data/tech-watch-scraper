# YouTube Tech Scraper

## Project Overview

A Python-based scraper that collects relevant content from multiple sources
(YouTube, RSS, GitHub) for technology monitoring and generates markdown reports
for import into NotebookLM.

## Target Topics

1. Claude AI tutorials
2. PySpark tutorials
3. Databricks tutorials

Each topic generates a separate markdown file with video metadata.

## Technical Stack

- Python 3.12
- UV for package management
- YouTube Data API v3
- Anthropic Claude API (for video filtering)
- GitHub Actions (for automated scheduling)
- Docker for containerization

## Output Format

For each topic, generate a markdown file containing:

- Video title
- Video URL
- Channel name
- Publication date
- Description (first 200 characters)
- View count

## Code Guidelines

- All entity names (variables, functions, classes, methods) in English
- Google-style docstrings with modern type hints
- Prefer explicit over implicit
- Use UV for dependency management

## Project Structure

```
youtube-tech-scraper/
├── CLAUDE.md
├── src/
│   ├── __init__.py
│   ├── scraper.py       # YouTube API interaction
│   ├── filter.py        # Claude API video filtering
│   ├── formatter.py     # Markdown generation
│   └── config.py        # Configuration (API keys, topics)
├── outputs/             # Generated markdown files
├── .github/workflows/   # GitHub Actions workflows
│   ├── ci.yml          # Code quality checks
│   ├── release.yml     # Automated releases
│   └── daily-scrape.yml # Daily automated scraping
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml       # UV project config
└── README.md
```

## Requirements

1. Use YouTube Data API v3 (user will provide API key via environment variable)
2. Rate limiting: respect YouTube API quotas
3. Error handling: graceful failures if API errors occur
4. Configurable: number of videos per topic (default: 10 most recent)
5. Sorting: videos by relevance to topic, then by date (newest first)

## Environment Variables

- `YOUTUBE_API_KEY`: YouTube Data API v3 key (required)
- `ANTHROPIC_API_KEY`: Anthropic API key (optional, required for filtering)

## Implementation Phases

### Phase 1: Core YouTube Scraping (Completed)

Implemented core functionality for YouTube video scraping:
- YouTube Data API v3 integration
- CLI with argparse
- Markdown report generation
- Configurable topics and result limits
- Error handling and logging

### Phase 2: AI Filtering & Automation (Completed)

Implemented Claude API filtering and GitHub Actions scheduling:

#### Video Filtering (src/filter.py)
- `VideoFilter` class using Claude API (claude-3-5-sonnet-20241022)
- Scoring system (0-10 scale):
  - Topic relevance: 0-4 points
  - Content quality: 0-3 points
  - Recency: 0-3 points
- `score_video()`: Evaluates individual videos
- `filter_videos()`: Batch filtering with statistics

#### CLI Integration
- `--filter-threshold` option (0-10 range)
- Filtering applied after scraping, before formatting
- Detailed logging with filtering statistics
- Only videos above threshold are saved

#### GitHub Actions Scheduling
- Daily automated runs at 9 AM UTC
- Manual workflow trigger with configurable parameters
- Artifact uploads (90-day retention)
- Summary generation for GitHub Actions UI

#### Configuration Updates
- Added `anthropic_api_key` to Config class
- Added `filter_enabled` and `filter_threshold` settings
- Validation for required API keys when filtering is enabled
