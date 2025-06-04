from typing import List

from fastapi import FastAPI, HTTPException

from config import DEFAULT_LIMIT_PER_CHAT
from telethon_handlers import export_chat_list, export_all_chats_media
from api_helpers import start_qr_login, check_qr_login, get_active_client

app = FastAPI(title="Telegram Downloader API")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/login/start")
async def login_start():
    return await start_qr_login()


@app.post("/login/status")
async def login_status(password: str | None = None):
    return await check_qr_login(password)


@app.post("/chats/export")
async def chats_export():
    client = get_active_client()
    if not client:
        raise HTTPException(status_code=400, detail="not_authenticated")
    chats = await export_chat_list(client)
    return {"count": len(chats), "chats": chats}


@app.post("/media/download")
async def media_download(chat_ids: List[int], limit: int = DEFAULT_LIMIT_PER_CHAT):
    client = get_active_client()
    if not client:
        raise HTTPException(status_code=400, detail="not_authenticated")
    chat_list = [{"id": cid, "title": str(cid), "type": "Unknown"} for cid in chat_ids]
    success, failed = await export_all_chats_media(client, chat_list, limit)
    return {"success": success, "failed": failed}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
