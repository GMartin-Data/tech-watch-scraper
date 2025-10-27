"""Configuration management for YouTube Tech Scraper."""

import os


class Config:
    """Configuration settings for the YouTube scraper.

    Attributes:
        youtube_api_key: YouTube Data API v3 key from environment variable.
        default_topics: Default technology topics to search for.
        max_results_per_topic: Maximum number of videos to fetch per topic.
        output_directory: Directory where markdown reports are saved.
    """

    def __init__(self) -> None:
        """Initialize configuration from environment variables and defaults."""
        self.youtube_api_key: str = os.getenv("YOUTUBE_API_KEY", "")
        self.default_topics: list[str] = [
            "Claude AI tutorials",
            "PySpark tutorials",
            "Databricks tutorials",
        ]
        self.max_results_per_topic: int = 10
        self.output_directory: str = "outputs"

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

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory, exist_ok=True)
