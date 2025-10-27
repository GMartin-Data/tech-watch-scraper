"""YouTube Tech Scraper CLI entry point."""

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.config import Config
from src.formatter import MarkdownFormatter
from src.scraper import YouTubeScraper


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="YouTube Tech Scraper - Collect YouTube videos for tech topics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default topics (Claude AI, PySpark, Databricks)
  python main.py

  # Search for specific topics
  python main.py "Python tutorials" "Machine Learning basics"

  # Change number of results per topic
  python main.py --max-results 20 "Docker tutorials"

  # Enable debug logging
  python main.py --log-level DEBUG "Kubernetes tutorials"
        """,
    )

    parser.add_argument(
        "topics",
        nargs="*",
        help="Topics to search for (if not provided, uses default topics)",
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum number of videos per topic (default: 10)",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory for output files (default: outputs)",
    )

    return parser.parse_args()


def sanitize_filename(topic: str) -> str:
    """Convert topic string to valid filename.

    Args:
        topic: Topic string to convert.

    Returns:
        Sanitized filename string.
    """
    # Replace spaces and special characters
    filename = topic.lower().replace(" ", "_")
    filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-"))
    return f"{filename}.md"


def main() -> None:
    """Main CLI entry point for YouTube Tech Scraper."""
    # Load environment variables from .env file
    load_dotenv()

    # Parse command-line arguments
    args = parse_arguments()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    try:
        # Initialize configuration
        config = Config()
        config.output_directory = args.output_dir
        config.max_results_per_topic = args.max_results
        config.validate()

        # Determine topics to search
        topics: list[str] = args.topics if args.topics else config.default_topics

        logger.info("=" * 70)
        logger.info("🚀 YouTube Tech Scraper Starting")
        logger.info("=" * 70)
        logger.info(f"📋 Topics to search: {len(topics)}")
        logger.info(f"📊 Max results per topic: {config.max_results_per_topic}")
        logger.info(f"📁 Output directory: {config.output_directory}")
        logger.info("=" * 70)

        # Initialize scraper and formatter
        scraper = YouTubeScraper(config.youtube_api_key)
        formatter = MarkdownFormatter()

        # Process each topic
        total_videos = 0
        for topic in topics:
            logger.info(f"\n⏳ Processing topic: {topic}")

            try:
                # Search for videos
                videos = scraper.search_videos(topic, config.max_results_per_topic)

                if not videos:
                    logger.warning(f"⚠️ No videos found for topic: {topic}")
                    continue

                # Generate output filename
                filename = sanitize_filename(topic)
                filepath = Path(config.output_directory) / filename

                # Save markdown report
                formatter.save_to_file(str(filepath), topic, videos)

                total_videos += len(videos)
                logger.info(f"✅ Saved {len(videos)} videos to {filepath}")

            except Exception as e:
                logger.error(f"❌ Failed to process topic '{topic}': {e}")
                continue

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("🎉 Scraping Complete!")
        logger.info(f"📊 Total topics processed: {len(topics)}")
        logger.info(f"📊 Total videos collected: {total_videos}")
        logger.info(f"💾 Reports saved to: {config.output_directory}/")
        logger.info("=" * 70)

    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
