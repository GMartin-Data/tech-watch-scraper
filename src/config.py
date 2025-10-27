"""Configuration management for YouTube Tech Scraper."""

import os


class Config:
    """Configuration settings for the YouTube scraper.

    Attributes:
        youtube_api_key: YouTube Data API v3 key from environment variable.
        anthropic_api_key: Anthropic API key for video filtering (optional).
        default_topics: Default technology topics to search for.
        max_results_per_topic: Maximum number of videos to fetch per topic.
        output_directory: Directory where markdown reports are saved.
        filter_enabled: Whether to enable Claude API filtering.
        filter_threshold: Minimum score (0-10) for videos to pass filtering.
    """

    def __init__(self) -> None:
        """Initialize configuration from environment variables and defaults."""
        self.youtube_api_key: str = os.getenv("YOUTUBE_API_KEY", "")
        self.anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
        self.default_topics: list[str] = [
            "Claude AI tutorials",
            "PySpark tutorials",
            "Databricks tutorials",
        ]
        self.max_results_per_topic: int = 10
        self.output_directory: str = "outputs"
        self.filter_enabled: bool = False
        self.filter_threshold: float = 7.0

    def validate(self) -> None:
        """Validate configuration settings.

        Raises:
            ValueError: If required configuration is missing or invalid.
        """
        if not self.youtube_api_key:
            raise ValueError(
                "❌ YOUTUBE_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )

        if self.filter_enabled and not self.anthropic_api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY required when filtering enabled. "
                "Set it in .env or disable filtering."
            )

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory, exist_ok=True)
