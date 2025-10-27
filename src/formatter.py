"""Markdown report generation for YouTube video data."""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class MarkdownFormatter:
    """Formatter for generating markdown reports from video data.

    This class converts YouTube video metadata into structured markdown
    files suitable for import into NotebookLM or other documentation tools.
    """

    @staticmethod
    def format_date(date_string: str) -> str:
        """Format ISO 8601 date string to readable format.

        Args:
            date_string: ISO 8601 formatted date string.

        Returns:
            Human-readable date string (e.g., "January 15, 2024").
        """
        try:
            date_obj = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            return date_obj.strftime("%B %d, %Y")
        except (ValueError, AttributeError):
            return date_string

    @staticmethod
    def format_view_count(view_count: int) -> str:
        """Format view count with thousands separators.

        Args:
            view_count: Number of views.

        Returns:
            Formatted view count string (e.g., "1,234,567").
        """
        return f"{view_count:,}"

    def generate_markdown(self, topic: str, videos: list[dict[str, Any]]) -> str:
        """Generate markdown content for a list of videos.

        Args:
            topic: The topic/search query used to find videos.
            videos: List of video metadata dictionaries.

        Returns:
            Formatted markdown string containing all video information.
        """
        logger.info(f"📝 Generating markdown for topic: {topic}")
        logger.debug(f"🪳 Processing {len(videos)} videos")

        # Create header
        markdown_lines = [
            f"# {topic}",
            "",
            f"*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*",
            "",
            f"Total videos: {len(videos)}",
            "",
            "---",
            "",
        ]

        # Add each video
        for idx, video in enumerate(videos, 1):
            video_section = self._format_video_section(idx, video)
            markdown_lines.extend(video_section)
            title = video.get("title", "Untitled")[:50]
            logger.debug(f"🪳 Formatted video {idx}/{len(videos)}: {title}")

        markdown_content = "\n".join(markdown_lines)
        logger.debug(f"🪳 Generated {len(markdown_lines)} lines of markdown")

        return markdown_content

    def _format_video_section(self, index: int, video: dict[str, Any]) -> list[str]:
        """Format a single video entry as markdown.

        Args:
            index: Video number in the list.
            video: Video metadata dictionary.

        Returns:
            List of markdown lines for the video entry.
        """
        return [
            f"## {index}. {video.get('title', 'Untitled')}",
            "",
            f"**URL:** [{video.get('url', '')}]({video.get('url', '')})",
            "",
            f"**Channel:** {video.get('channel_name', 'Unknown')}",
            "",
            f"**Published:** {self.format_date(video.get('published_at', ''))}",
            "",
            f"**Views:** {self.format_view_count(video.get('view_count', 0))}",
            "",
            "**Description:**",
            "",
            f"> {video.get('description', 'No description available.')}",
            "",
            "---",
            "",
        ]

    def save_to_file(
        self, filepath: str, topic: str, videos: list[dict[str, Any]]
    ) -> None:
        """Generate and save markdown report to a file.

        Args:
            filepath: Path where the markdown file should be saved.
            topic: The topic/search query used to find videos.
            videos: List of video metadata dictionaries.

        Raises:
            IOError: If file cannot be written.
        """
        try:
            logger.debug(f"🪳 Saving markdown to: {filepath}")
            markdown_content = self.generate_markdown(topic, videos)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            logger.info(f"💾 Saved markdown report to: {filepath}")

        except OSError as e:
            logger.error(f"❌ Failed to save markdown to {filepath}: {e}")
            raise
