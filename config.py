
"""
Configuration module for Telegram Media Downloader
Contains API credentials and application settings
"""

import os

# Telegram API credentials - Replace with your actual values
# Get these from https://my.telegram.org/apps
API_ID = 27031784  # Replace with your API ID
API_HASH = '8a5c5a5d72783ac32fc40426b2a4316c'  # Replace with your API Hash

# Application settings
SESSION_NAME = "telegram_downloader_session"
EXPORTS_DIR = "exports"
DEFAULT_LIMIT_PER_CHAT = 1000

# File size limits (in bytes)
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB default limit

# Download settings
ENABLE_PROGRESS_BAR = True
CONCURRENT_DOWNLOADS = 1  # Keep at 1 to avoid rate limiting

# Supported media types
SUPPORTED_MEDIA_TYPES = [
    'photo', 'video', 'document', 'audio', 'voice', 'sticker'
]

# Directory names for different media types
MEDIA_DIRECTORIES = {
    'photo': 'fotos',
    'video': 'videos',
    'document': 'documentos',
    'audio': 'audio',
    'voice': 'mensagens_voz',
    'sticker': 'stickers',
    'other': 'outros'
}
