# Telegram Downloader API

Esta API expõe funcionalidades básicas do projeto via HTTP utilizando FastAPI.

## Endpoints

### `POST /login/start`
Inicia o processo de login via QR Code.
- **Resposta**: `{ "authorized": bool, "qr_url": "<url>" }`

### `POST /login/status`
Verifica o status do login. Envie `password` no corpo para completar a 2FA quando necessário.
- **Body**: `{"password": "opcional"}`
- **Resposta**:
  - Quando logado: `{ "authorized": true }`
  - Aguardando leitura do QR: `{ "authorized": false }`

### `POST /chats/export`
Exporta a lista de chats do usuário autenticado.
- **Resposta**: `{ "count": <int>, "chats": [ ... ] }`

### `POST /media/download`
Realiza o download das mídias dos chats informados.
- **Body**: `{"chat_ids": [123456, 78910], "limit": 100}`
- **Resposta**: `{ "success": <int>, "failed": <int> }`

### `GET /health`
Endpoint simples para verificação de status.
- **Resposta**: `{ "status": "ok" }`
