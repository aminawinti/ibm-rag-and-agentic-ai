import re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi

from config import CHUNK_OVERLAP, CHUNK_SIZE, YOUTUBE_URL_PATTERN


def get_video_id(url):
    match = re.search(YOUTUBE_URL_PATTERN, url)
    return match.group(1) if match else None


def get_transcript(url):
    video_id = get_video_id(url)
    if not video_id:
        return None

    transcript = None
    for t in YouTubeTranscriptApi().list(video_id):
        if t.language_code != "en":
            continue
        if not t.is_generated:
            return t.fetch()  # a manual transcript beats an auto-generated one, stop looking
        if transcript is None:
            transcript = t.fetch()  # keep the auto-generated one as a fallback
    return transcript


def format_transcript(transcript):
    lines = ""
    for entry in transcript:
        try:
            # older api versions return dicts, newer ones return objects
            if isinstance(entry, dict):
                text, start = entry["text"], entry["start"]
            else:
                text, start = entry.text, entry.start
            lines += f"Text: {text} Start: {start}\n"
        except (KeyError, AttributeError):
            continue
    return lines


def load_transcript(url):
    # cached per url, so summary and Q&A on the same video fetch it once
    transcript = get_transcript(url)
    return format_transcript(transcript) if transcript else ""


def chunk_transcript(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_text(text)
