"""YouTube API interaction for fetching video data."""

import logging
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class YouTubeScraper:
    """YouTube scraper using YouTube Data API v3.

    Attributes:
        api_key: YouTube Data API v3 key.
        youtube: YouTube API service instance.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize YouTube scraper with API key.

        Args:
            api_key: YouTube Data API v3 key.

        Raises:
            ValueError: If api_key is empty or invalid.
        """
        if not api_key:
            raise ValueError("YouTube API key is required")

        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
        logger.info("✅ YouTube scraper initialized successfully")

    def search_videos(self, topic: str, max_results: int = 10) -> list[dict[str, Any]]:
        """Search for videos related to a specific topic.

        Args:
            topic: The search query/topic to find videos for.
            max_results: Maximum number of videos to retrieve (default: 10).

        Returns:
            List of video data dictionaries containing metadata.

        Raises:
            HttpError: If YouTube API request fails.
        """
        try:
            logger.info(f"🔍 Searching for videos about: {topic}")

            # Search for videos
            logger.debug(f"🪳 Requesting search with max_results={max_results}")
            search_response = (
                self.youtube.search()
                .list(
                    q=topic,
                    part="id,snippet",
                    maxResults=max_results,
                    type="video",
                    order="relevance",  # Sort by relevance first
                    relevanceLanguage="en",
                )
                .execute()
            )

            video_ids = [
                item["id"]["videoId"] for item in search_response.get("items", [])
            ]
            logger.debug(f"🪳 Retrieved {len(video_ids)} video IDs from search")

            if not video_ids:
                logger.warning(f"⚠️ No videos found for topic: {topic}")
                return []

            # Get detailed video statistics
            logger.debug(f"🪳 Fetching video details for {len(video_ids)} videos")
            videos_response = (
                self.youtube.videos()
                .list(part="snippet,statistics", id=",".join(video_ids))
                .execute()
            )

            videos_data = []
            for item in videos_response.get("items", []):
                video_data = self._extract_video_data(item)
                videos_data.append(video_data)

            # Sort by publication date (newest first) after relevance
            videos_data.sort(key=lambda x: x.get("published_at", ""), reverse=True)
            logger.debug("🪳 Sorted videos by publication date")

            logger.info(f"✅ Found {len(videos_data)} videos for topic: {topic}")
            return videos_data

        except HttpError as e:
            logger.error(f"❌ YouTube API error for topic '{topic}': {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error searching for topic '{topic}': {e}")
            raise

    def _extract_video_data(self, video_item: dict[str, Any]) -> dict[str, Any]:
        """Extract relevant video metadata from API response.

        Args:
            video_item: Raw video item from YouTube API response.

        Returns:
            Dictionary containing extracted video metadata.
        """
        snippet = video_item.get("snippet", {})
        statistics = video_item.get("statistics", {})

        # Get description and truncate to 200 characters
        description = snippet.get("description", "")
        description_truncated = (
            description[:200] + "..." if len(description) > 200 else description
        )

        return {
            "video_id": video_item.get("id", ""),
            "title": snippet.get("title", ""),
            "url": f"https://www.youtube.com/watch?v={video_item.get('id', '')}",
            "channel_name": snippet.get("channelTitle", ""),
            "published_at": snippet.get("publishedAt", ""),
            "description": description_truncated,
            "view_count": int(statistics.get("viewCount", 0)),
        }
