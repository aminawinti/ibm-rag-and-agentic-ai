import logging
import re
from typing import Dict, List

import yt_dlp
from langchain_core.tools import tool
from pytube import Search
from youtube_transcript_api import YouTubeTranscriptApi

# pytube and yt-dlp are noisy; only real errors are interesting
logging.getLogger("pytube").setLevel(logging.ERROR)
yt_dlp_logger = logging.getLogger("yt_dlp")
yt_dlp_logger.setLevel(logging.ERROR)


@tool
def extract_video_id(url: str) -> str:
    """
    Extracts the 11-character YouTube video ID from a URL.

    Args:
        url (str): A YouTube URL containing a video ID.

    Returns:
        str: Extracted video ID or error message if parsing fails.
    """
    match = re.search(r"(?:v=|be/|embed/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else "Error: Invalid YouTube URL"


@tool
def fetch_transcript(video_id: str, language: str = "en") -> str:
    """
    Fetches the transcript of a YouTube video.

    Args:
        video_id (str): The YouTube video ID (e.g., "dQw4w9WgXcQ").
        language (str): Language code for the transcript (e.g., "en", "es").

    Returns:
        str: The transcript text or an error message.
    """
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=[language])
        return " ".join(snippet.text for snippet in transcript.snippets)
    except Exception as e:
        return f"Error: {e}"


@tool
def search_youtube(query: str) -> List[Dict[str, str]]:
    """
    Search YouTube for videos matching the query.

    Args:
        query (str): The search term to look for on YouTube

    Returns:
        List of dictionaries with video title, video_id and url.
        Returns an error message if the search fails.
    """
    try:
        return [
            {
                "title": yt.title,
                "video_id": yt.video_id,
                "url": f"https://youtu.be/{yt.video_id}",
            }
            for yt in Search(query).results
        ]
    except Exception as e:
        return f"Error: {e}"


@tool
def get_full_metadata(url: str) -> dict:
    """Extract metadata given a YouTube URL, including title, views, duration, channel, likes, comments, and chapters."""
    with yt_dlp.YoutubeDL({"quiet": True, "logger": yt_dlp_logger}) as ydl:
        info = ydl.extract_info(url, download=False)  # metadata only, no download
        return {
            "title": info.get("title"),
            "views": info.get("view_count"),
            "duration": info.get("duration"),
            "channel": info.get("uploader"),
            "likes": info.get("like_count"),
            "comments": info.get("comment_count"),
            "chapters": info.get("chapters", []),
        }


@tool
def get_thumbnails(url: str) -> List[Dict]:
    """
    Get available thumbnails for a YouTube video using its URL.

    Args:
        url (str): YouTube video URL (any format)

    Returns:
        List of dictionaries with thumbnail URLs and resolutions in YouTube's native order
    """
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "logger": yt_dlp_logger}) as ydl:
            info = ydl.extract_info(url, download=False)
            return [
                {
                    "url": t["url"],
                    "width": t.get("width"),
                    "height": t.get("height"),
                    "resolution": f"{t.get('width', '')}x{t.get('height', '')}".strip("x"),
                }
                for t in info.get("thumbnails", [])
                if "url" in t
            ]
    except Exception as e:
        return [{"error": f"Failed to get thumbnails: {e}"}]


# tools bound to the LLM
tools = [extract_video_id, fetch_transcript, search_youtube, get_full_metadata, get_thumbnails]

# map the tool name to the real tool object
tool_mapping = {t.name: t for t in tools}
