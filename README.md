# Tech Watch Scraper

[![CI](https://github.com/GMartin-Data/tech-watch-scraper/workflows/CI/badge.svg)](https://github.com/GMartin-Data/tech-watch-scraper/actions)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A Python-based scraper that collects relevant YouTube videos for technology topics and generates markdown reports for import into NotebookLM.

## Features

- Search YouTube for technology-related videos using YouTube Data API v3
- Generate structured markdown reports with video metadata
- Support for multiple topics in a single run
- Configurable number of results per topic
- Simple CLI interface with sensible defaults
- Emoji logging for better visual debugging

## Prerequisites

- Python 3.12 or higher
- UV package manager ([installation guide](https://docs.astral.sh/uv/))
- YouTube Data API v3 key ([get one here](https://console.cloud.google.com/apis/credentials))

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/GMartin-Data/tech-watch-scraper.git
   cd tech-watch-scraper
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root:
   ```bash
   echo "YOUTUBE_API_KEY=your_api_key_here" > .env
   ```

## Usage

### Basic Usage

Run with default topics (Claude AI, PySpark, Databricks):

```bash
uv run python main.py
```

### Custom Topics

Search for specific topics:

```bash
uv run python main.py "Python tutorials" "Machine Learning basics"
```

### Advanced Options

Change the number of results per topic:

```bash
uv run python main.py --max-results 20 "Docker tutorials"
```

Enable debug logging:

```bash
uv run python main.py --log-level DEBUG "Kubernetes tutorials"
```

Specify a custom output directory:

```bash
uv run python main.py --output-dir reports "AI tutorials"
```

## Output Format

For each topic, the scraper generates a markdown file in the `outputs/` directory containing:

- Video title
- Video URL (clickable link)
- Channel name
- Publication date
- View count (formatted with thousands separators)
- Description (first 200 characters)

Example output filename: `claude_ai_tutorials.md`

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines including:

- Code quality standards (Ruff)
- Conventional commits format
- Feature branch workflow
- Pre-commit hooks

### Quick Development Workflow

```bash
# Create a new feature branch
./scripts/new-feature.sh my-feature

# Make changes, then check code quality
./scripts/lint.sh --fix

# Commit with conventional format
git add .
uv run cz commit

# Push and create PR
git push -u origin feature/my-feature
```

## Project Structure

```
tech-watch-scraper/
├── CLAUDE.md              # Project specification
├── README.md              # This file
├── main.py                # CLI entry point
├── pyproject.toml         # UV project configuration
├── src/
│   ├── config.py          # Configuration management
│   ├── scraper.py         # YouTube API interaction
│   └── formatter.py       # Markdown generation
├── outputs/               # Generated markdown files
├── scripts/               # Helper scripts
│   ├── lint.sh           # Run code quality checks
│   ├── bump.sh           # Bump version
│   └── new-feature.sh    # Create feature branch
└── .github/workflows/     # CI/CD workflows
    ├── ci.yml            # Code quality checks
    └── release.yml       # Automated releases
```

## License

MIT

