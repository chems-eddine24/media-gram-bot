import os
import re
import asyncio
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError

DOWNLOADS_DIR = Path("downloads")
PLATFORM_PATTERNS = {
    "youtube": re.compile(r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[\w\-]+"),
    "tiktok": re.compile(r"(https?://)?(www\.|vm\.)?tiktok\.com/[\w\-/@]+"),
    "instagram": re.compile(r"(https?://)?(www\.)?instagram\.com/(p|reel|tv)/[\w\-]+"),
    "facebook": re.compile(r"(https?://)?(www\.|m\.)?facebook\.com/[\w\-/]+/videos/[\w\-]+"),
}


def detect_platform(url: str) -> str | None:
    for platform, pattern in PLATFORM_PATTERNS.items():
        if pattern.search(url):
            return platform
    return None


def _ensure_downloads_dir() -> None:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)


def _download_video_sync(url: str, quality: str = "best") -> str:
    _ensure_downloads_dir()

    format_str = (
        f"bestvideo[height<={quality}]+bestaudio/best"
        if quality != "best"
        else "bestvideo+bestaudio/best"
    )

    ydl_opts = {
        "format": format_str,
        "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base = os.path.splitext(filename)[0]
        return base + ".mp4" if not filename.endswith(".mp4") else filename


def _download_audio_sync(url: str) -> str:
    _ensure_downloads_dir()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".mp3"


async def download_video(url: str, quality: str = "best") -> str:
    try:
        return await asyncio.get_event_loop().run_in_executor(
            None, _download_video_sync, url, quality
        )
    except DownloadError as e:
        raise ValueError(f"Could not download video: {e}") from e
    except ExtractorError as e:
        raise ValueError(f"Could not extract info from URL: {e}") from e


async def download_audio(url: str) -> str:
    try:
        return await asyncio.get_event_loop().run_in_executor(
            None, _download_audio_sync, url
        )
    except DownloadError as e:
        raise ValueError(f"Could not download audio: {e}") from e
    except ExtractorError as e:
        raise ValueError(f"Could not extract info from URL: {e}") from e