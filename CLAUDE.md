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
│   ├── formatter.py     # Markdown generation
│   └── config.py        # Configuration (API key, topics)
├── outputs/             # Generated markdown files
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
