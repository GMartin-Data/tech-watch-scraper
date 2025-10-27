# Tech Watch Scraper

[![CI](https://github.com/GMartin-Data/tech-watch-scraper/workflows/CI/badge.svg)](https://github.com/GMartin-Data/tech-watch-scraper/actions)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A Python-based scraper that collects relevant YouTube videos for technology topics and generates markdown reports for import into NotebookLM.

## Features

- Search YouTube for technology-related videos using YouTube Data API v3
- **AI-powered filtering** using Claude API to score videos for relevance and quality
- Generate structured markdown reports with video metadata
- Support for multiple topics in a single run
- Configurable number of results per topic
- Simple CLI interface with sensible defaults
- Automated daily scraping via GitHub Actions
- Emoji logging for better visual debugging

## Prerequisites

- Python 3.12 or higher
- UV package manager ([installation guide](https://docs.astral.sh/uv/))
- YouTube Data API v3 key ([get one here](https://console.cloud.google.com/apis/credentials))
- Anthropic API key (optional, for video filtering) ([get one here](https://console.anthropic.com/))

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
   cp .env.example .env
   # Edit .env and add your API keys
   ```

   Required environment variables:
   - `YOUTUBE_API_KEY`: Your YouTube Data API v3 key (required)
   - `ANTHROPIC_API_KEY`: Your Anthropic API key (optional, only for filtering)

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

### AI-Powered Filtering

Enable Claude API filtering to score and filter videos based on relevance, quality, and recency:

```bash
uv run python main.py --filter-threshold 7 "Python tutorials"
```

The filtering system evaluates videos on a 0-10 scale:
- **Topic Relevance** (0-4 points): How well the video matches the search topic
- **Content Quality** (0-3 points): Educational value, production quality, credibility
- **Recency** (0-3 points): How recent the content is (favors newer videos)

Only videos scoring at or above the threshold are included in the output.

**Examples:**

```bash
# Filter with default threshold of 7/10
uv run python main.py --filter-threshold 7

# Stricter filtering (only highly relevant videos)
uv run python main.py --filter-threshold 9 "Machine Learning tutorials"

# Combine with more initial results for better filtered output
uv run python main.py --max-results 20 --filter-threshold 8 "Docker tutorials"
```

**Note:** Filtering requires an Anthropic API key. Each video scored consumes API tokens.

## Output Format

For each topic, the scraper generates a markdown file in the `outputs/` directory containing:

- Video title
- Video URL (clickable link)
- Channel name
- Publication date
- View count (formatted with thousands separators)
- Description (first 200 characters)

Example output filename: `claude_ai_tutorials.md`

## Automated Scheduling

The project includes a GitHub Actions workflow for automated daily scraping at 9 AM UTC.

### Setup

1. Add repository secrets in GitHub Settings > Secrets and variables > Actions:
   - `YOUTUBE_API_KEY`: Your YouTube Data API v3 key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key

2. The workflow will run automatically every day at 9 AM UTC

3. Results are saved as workflow artifacts (retained for 90 days)

### Manual Trigger

You can manually trigger the workflow from the Actions tab:

1. Go to Actions > Daily YouTube Scrape
2. Click "Run workflow"
3. Optionally customize:
   - Filter threshold (default: 7)
   - Max results per topic (default: 10)

### Workflow Configuration

See [.github/workflows/daily-scrape.yml](.github/workflows/daily-scrape.yml) for details. The workflow:
- Runs daily at 9 AM UTC
- Uses filtering by default (threshold: 7)
- Uploads results as artifacts
- Provides a summary of generated reports

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
│   ├── filter.py          # Claude API video filtering
│   └── formatter.py       # Markdown generation
├── outputs/               # Generated markdown files
├── scripts/               # Helper scripts
│   ├── lint.sh           # Run code quality checks
│   ├── bump.sh           # Bump version
│   └── new-feature.sh    # Create feature branch
└── .github/workflows/     # CI/CD workflows
    ├── ci.yml            # Code quality checks
    ├── release.yml       # Automated releases
    └── daily-scrape.yml  # Daily automated scraping
```

## License

MIT

