"""Configuration handling for Telegram Media Downloader."""

import os
import logging
from dataclasses import dataclass, field
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    API_ID: int = int(os.getenv("API_ID", "12345"))
    API_HASH: str = os.getenv(
        "API_HASH", "0123456789abcdef0123456789abcdef"
    )

    SESSION_NAME: str = os.getenv("SESSION_NAME", "telegram_downloader_session")
    EXPORTS_DIR: str = os.getenv("EXPORTS_DIR", "exports")
    DEFAULT_LIMIT_PER_CHAT: int = int(os.getenv("DEFAULT_LIMIT_PER_CHAT", "1000"))

    MAX_FILE_SIZE: int = int(
        os.getenv("MAX_FILE_SIZE", str(1024 * 1024 * 1024))
    )  # 1GB

    ENABLE_PROGRESS_BAR: bool = os.getenv("ENABLE_PROGRESS_BAR", "True") == "True"
    CONCURRENT_DOWNLOADS: int = int(os.getenv("CONCURRENT_DOWNLOADS", "1"))

    SUPPORTED_MEDIA_TYPES: List[str] = field(
        default_factory=lambda: [
            "photo",
            "video",
            "document",
            "audio",
            "voice",
            "sticker",
        ]
    )

    MEDIA_DIRECTORIES: Dict[str, str] = field(
        default_factory=lambda: {
            "photo": "fotos",
            "video": "videos",
            "document": "documentos",
            "audio": "audio",
            "voice": "mensagens_voz",
            "sticker": "stickers",
            "other": "outros",
        }
    )

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

# Backwards compatibility: expose variables
API_ID = settings.API_ID
API_HASH = settings.API_HASH
SESSION_NAME = settings.SESSION_NAME
EXPORTS_DIR = settings.EXPORTS_DIR
DEFAULT_LIMIT_PER_CHAT = settings.DEFAULT_LIMIT_PER_CHAT
MAX_FILE_SIZE = settings.MAX_FILE_SIZE
ENABLE_PROGRESS_BAR = settings.ENABLE_PROGRESS_BAR
CONCURRENT_DOWNLOADS = settings.CONCURRENT_DOWNLOADS
SUPPORTED_MEDIA_TYPES = settings.SUPPORTED_MEDIA_TYPES
MEDIA_DIRECTORIES = settings.MEDIA_DIRECTORIES
LOG_LEVEL = settings.LOG_LEVEL


def configure_logging() -> None:
    """Configure basic logging for the application."""

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


configure_logging()

