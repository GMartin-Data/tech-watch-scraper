"""Claude API-based video filtering for quality and relevance scoring."""

import logging
from typing import Any

from anthropic import Anthropic

logger = logging.getLogger(__name__)


class VideoFilter:
    """Filter videos using Claude API for relevance and quality scoring.

    Attributes:
        client: Anthropic API client instance.
        model: Claude model to use for scoring (default: claude-3-7-sonnet-20250219).
    """

    def __init__(self, api_key: str, model: str = "claude-3-7-sonnet-20250219") -> None:
        """Initialize video filter with Anthropic API key.

        Args:
            api_key: Anthropic API key for Claude API access.
            model: Claude model to use for scoring.

        Raises:
            ValueError: If api_key is empty or invalid.
        """
        if not api_key:
            raise ValueError("Anthropic API key is required")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        logger.info("✅ Video filter initialized successfully")

    def score_video(self, video: dict[str, Any], topic: str) -> dict[str, Any]:
        """Score a video for relevance and quality using Claude API.

        The scoring system evaluates:
        - Topic relevance (0-4 points): How well video matches the search topic
        - Content quality (0-3 points): Educational value, production quality,
          credibility
        - Recency (0-3 points): How recent the content is (favors newer videos)

        Args:
            video: Video data dictionary with metadata.
            topic: Search topic to evaluate relevance against.

        Returns:
            Dictionary containing:
                - score: Total score (0-10)
                - reasoning: Explanation of the score
                - breakdown: Score breakdown by category

        Raises:
            Exception: If Claude API request fails.
        """
        try:
            # Prepare video context for Claude
            video_context = self._prepare_video_context(video, topic)

            # Call Claude API for scoring
            logger.debug(f"🤖 Scoring video: {video.get('title', 'Unknown')}")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.0,  # Deterministic scoring
                messages=[
                    {
                        "role": "user",
                        "content": video_context,
                    }
                ],
            )

            # Parse response
            response_text = message.content[0].text
            score_result = self._parse_claude_response(response_text)

            title = video.get("title", "Unknown")[:40]
            logger.debug(f"📊 Video scored: {score_result['score']}/10 - {title}...")
            return score_result

        except Exception as e:
            title = video.get("title", "Unknown")
            logger.error(f"❌ Error scoring video '{title}': {e}")
            raise

    def _prepare_video_context(self, video: dict[str, Any], topic: str) -> str:
        """Prepare video context string for Claude API.

        Args:
            video: Video data dictionary.
            topic: Search topic.

        Returns:
            Formatted context string for Claude.
        """
        return f"""You are a video quality and relevance evaluator. 
        Score this YouTube video for a search about "{topic}".

        Video Details:
        - Title: {video.get("title", "N/A")}
        - Channel: {video.get("channel_name", "N/A")}
        - Published: {video.get("published_at", "N/A")}
        - Views: {video.get("view_count", 0):,}
        - Description: {video.get("description", "N/A")}

        Scoring Criteria:
        1. Topic Relevance (0-4 points):
        - 4: Highly relevant, directly addresses the topic
        - 3: Very relevant, covers most aspects of the topic
        - 2: Moderately relevant, tangentially related
        - 1: Slightly relevant, barely related
        - 0: Not relevant at all

        2. Content Quality (0-3 points):
        - 3: High quality - professional, credible source, comprehensive
        - 2: Good quality - decent production, reliable information
        - 1: Fair quality - basic content, some value
        - 0: Poor quality - low value, questionable credibility

        3. Recency (0-3 points):
        - 3: Very recent (< 3 months old)
        - 2: Recent (3-12 months old)
        - 1: Somewhat recent (1-2 years old)
        - 0: Old (> 2 years old)

        Respond ONLY with a JSON object in this exact format:
        {{
            "topic_relevance": <0-4>,
            "content_quality": <0-3>,
            "recency": <0-3>,
            "total_score": <sum of above>,
            "reasoning": "<brief explanation of the scoring>"
        }}"""

    def _parse_claude_response(self, response_text: str) -> dict[str, Any]:
        """Parse Claude's response into structured score result.

        Args:
            response_text: Raw text response from Claude API.

        Returns:
            Dictionary with score, reasoning, and breakdown.

        Raises:
            ValueError: If response cannot be parsed.
        """
        import json

        try:
            # Extract JSON from response (handle markdown code blocks)
            response_text = response_text.strip()
            if "```json" in response_text:
                start = response_text.index("```json") + 7
                end = response_text.rindex("```")
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.index("```") + 3
                end = response_text.rindex("```")
                response_text = response_text[start:end].strip()

            # Parse JSON
            parsed = json.loads(response_text)

            return {
                "score": parsed.get("total_score", 0),
                "reasoning": parsed.get("reasoning", "No reasoning provided"),
                "breakdown": {
                    "topic_relevance": parsed.get("topic_relevance", 0),
                    "content_quality": parsed.get("content_quality", 0),
                    "recency": parsed.get("recency", 0),
                },
            }

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"❌ Failed to parse Claude response: {e}")
            logger.debug(f"Response text: {response_text}")
            raise ValueError(f"Invalid Claude API response format: {e}")

    def filter_videos(
        self,
        videos: list[dict[str, Any]],
        topic: str,
        threshold: float = 7.0,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Filter a list of videos based on quality threshold.

        Args:
            videos: List of video data dictionaries.
            topic: Search topic for relevance evaluation.
            threshold: Minimum score threshold (0-10) to keep videos.

        Returns:
            Tuple containing:
                - List of filtered videos (above threshold)
                - Statistics dictionary with filtering details
        """
        if not videos:
            return [], {"total": 0, "kept": 0, "filtered": 0}

        logger.info(f"🔍 Filtering {len(videos)} videos for topic: {topic}")

        filtered_videos = []
        scores = []

        for video in videos:
            try:
                score_result = self.score_video(video, topic)
                score = score_result["score"]
                scores.append(score)

                if score >= threshold:
                    # Add score metadata to video
                    video["filter_score"] = score
                    video["filter_reasoning"] = score_result["reasoning"]
                    video["filter_breakdown"] = score_result["breakdown"]
                    filtered_videos.append(video)

            except Exception as e:
                logger.warning(f"⚠️ Skipping video due to scoring error: {e}")
                continue

        stats = {
            "total": len(videos),
            "kept": len(filtered_videos),
            "filtered": len(videos) - len(filtered_videos),
            "threshold": threshold,
            "avg_score": sum(scores) / len(scores) if scores else 0,
        }

        logger.info(
            f"✅ Filtering complete: {stats['kept']} kept, "
            f"{stats['filtered']} filtered (threshold: {threshold})"
        )

        return filtered_videos, stats
