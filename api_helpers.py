from typing import Optional, Dict, Any

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import API_ID, API_HASH, SESSION_NAME

_active_client: Optional[TelegramClient] = None
_qr_login = None


async def start_qr_login() -> Dict[str, Any]:
    """Start QR code login and return the URL."""
    global _active_client, _qr_login

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()

    if await client.is_user_authorized():
        _active_client = client
        return {"authorized": True}

    _qr_login = await client.qr_login()
    _active_client = client
    return {"authorized": False, "qr_url": _qr_login.url}


async def check_qr_login(password: Optional[str] = None) -> Dict[str, Any]:
    """Check login status. Provide password if 2FA is required."""
    global _active_client, _qr_login

    if _active_client is None:
        return {"authorized": False, "detail": "login_not_started"}

    if _qr_login is None:
        authorized = await _active_client.is_user_authorized()
        return {"authorized": authorized}

    try:
        await _qr_login.wait(1)
    except TimeoutError:
        return {"authorized": False}
    except SessionPasswordNeededError:
        if password:
            await _active_client.sign_in(password=password)
        else:
            return {"authorized": False, "detail": "2fa_required"}
    except Exception as e:
        return {"authorized": False, "detail": str(e)}

    if await _active_client.is_user_authorized():
        _qr_login = None
        return {"authorized": True}
    return {"authorized": False}


def get_active_client() -> Optional[TelegramClient]:
    """Return the active authenticated client if available."""
    return _active_client
