"""
File utilities module for Telegram Media Downloader
Handles file and directory operations, sanitization, and organization
"""

import os
import re
from typing import Dict, List


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters from filename/directory name

    Args:
        filename: Original filename string

    Returns:
        Sanitized filename safe for filesystem use
    """
    # Invalid characters for most filesystems
    invalid_chars = '<>:"/\\|?*'

    # Replace invalid characters with underscore
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Remove leading/trailing whitespace and dots
    filename = filename.strip(" .")

    # Ensure filename is not empty
    if not filename:
        filename = "unnamed"

    # Limit length to 200 characters
    if len(filename) > 200:
        filename = filename[:200]

    return filename


def create_media_directories(base_path: str, topic_name: str = None) -> Dict[str, str]:
    """
    Create directory structure for organizing media files

    Args:
        base_path: Base directory path for the chat
        topic_name: Optional topic name for forum groups

    Returns:
        Dictionary mapping media types to their directory paths
    """
    from config import MEDIA_DIRECTORIES

    # Add topic subdirectory if specified
    topic_suffix = f"/{sanitize_filename(topic_name)}" if topic_name else ""

    media_dirs = {}
    for media_type, dir_name in MEDIA_DIRECTORIES.items():
        media_dirs[media_type] = f"{base_path}{topic_suffix}/{dir_name}"

    return media_dirs


def ensure_directories_exist(directories: Dict[str, str]) -> None:
    """
    Create all directories in the provided dictionary

    Args:
        directories: Dictionary of directory paths to create
    """
    for dir_path in directories.values():
        os.makedirs(dir_path, exist_ok=True)


def get_file_extension(message) -> str:
    """
    Determine appropriate file extension based on media type

    Args:
        message: Telethon message object with media

    Returns:
        File extension string including the dot
    """
    if message.photo:
        return ".jpg"
    elif message.video:
        return ".mp4"
    elif message.voice:
        return ".ogg"
    elif message.audio:
        return ".mp3"
    elif message.sticker:
        return ".webp"
    elif message.document:
        # Try to get extension from document attributes
        if hasattr(message.document, "attributes"):
            for attr in message.document.attributes:
                if hasattr(attr, "file_name") and attr.file_name:
                    _, ext = os.path.splitext(attr.file_name)
                    return ext if ext else ".bin"
        return ".bin"
    else:
        return ".bin"


def get_media_type_name(message) -> str:
    """
    Get the media type name for directory organization

    Args:
        message: Telethon message object with media

    Returns:
        Media type string for directory mapping
    """
    if message.photo:
        return "photo"
    elif message.video:
        return "video"
    elif message.voice:
        return "voice"
    elif message.audio:
        return "audio"
    elif message.sticker:
        return "sticker"
    elif message.document:
        return "document"
    else:
        return "other"


def generate_filename(message, topic_name: str = None) -> str:
    """
    Generate organized filename with timestamp and metadata

    Args:
        message: Telethon message object
        topic_name: Optional topic name for prefix

    Returns:
        Generated filename string
    """
    # Create timestamp from message date
    timestamp = message.date.strftime("%Y%m%d_%H%M%S")

    # Add topic prefix if specified
    topic_prefix = f"[{sanitize_filename(topic_name)}]_" if topic_name else ""

    # Get appropriate file extension
    extension = get_file_extension(message)

    # Generate final filename
    filename = f"{topic_prefix}{timestamp}_msg{message.id}{extension}"

    return filename


def write_download_log(
    log_file,
    filename: str,
    media_type: str,
    message_id: int,
    message_date,
    topic_name: str = None,
) -> None:
    """
    Write download operation to log file

    Args:
        log_file: Open file handle to append log entries
        filename: Downloaded filename
        media_type: Type of media downloaded
        message_id: Telegram message ID
        message_date: Message timestamp
        topic_name: Optional topic name
    """
    from datetime import datetime

    topic_info = f" - Tópico: {topic_name}" if topic_name else ""
    log_entry = (
        f"{datetime.now()}: {filename} - {media_type} - "
        f"Msg ID: {message_id} - Data: {message_date}{topic_info}\n"
    )

    log_file.write(log_entry)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math

    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"
