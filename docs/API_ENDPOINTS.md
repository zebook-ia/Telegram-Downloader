# Telegram Downloader API

Esta API expõe funcionalidades básicas do projeto via HTTP utilizando **FastAPI**.
Pode ser executada via Docker/Traefik, ficando acessível por uma URL pública.

## Endpoints

### `POST /login/start`
Inicia o fluxo de autenticação via QR Code.

**Resposta**
- Quando não autenticado: `{ "authorized": false, "qr_url": "<url>" }`
- Quando já autenticado: `{ "authorized": true }`

**Exemplo de uso**
```bash
curl -X POST https://seu-servidor/login/start
```

### `POST /login/status`
Verifica o estado atual do login e, opcionalmente, recebe a senha de 2FA.

**Body**
```json
{ "password": "opcional" }
```

**Resposta**
```json
{ "authorized": true }
```
ou
```json
{ "authorized": false }
```

**Exemplo de uso**
```bash
curl -X POST https://seu-servidor/login/status -d '{"password": "<senha-2fa>"}' \
  -H "Content-Type: application/json"
```

### `POST /chats/export`
Exporta a lista de chats do usuário autenticado.

**Resposta**
```json
{ "count": <int>, "chats": [...] }
```

**Exemplo de uso**
```bash
curl -X POST https://seu-servidor/chats/export
```

### `POST /media/download`
Recebe IDs dos chats cujas mídias serão baixadas. O parâmetro `limit` controla o número máximo de mensagens a processar.

**Body**
```json
{ "chat_ids": [123456, 78910], "limit": 100 }
```

**Resposta**
```json
{ "success": <int>, "failed": <int> }
```

**Exemplo de uso**
```bash
curl -X POST https://seu-servidor/media/download \
  -H "Content-Type: application/json" \
  -d '{"chat_ids": [123456], "limit": 50}'
```

### `GET /health`
Endpoint simples para verificar se o serviço está ativo.

**Resposta**
```json
{ "status": "ok" }
```

**Exemplo de uso**
```bash
curl https://seu-servidor/health
```

## Limitações e restrições

- **Rate limiting** – o Telegram impõe limites de requisições; faça pequenas pausas entre operações para evitar bloqueios.
- **Tamanho máximo de arquivo** – o limite padrão é 1 GB; conteúdos maiores podem gerar timeout.
- **Acesso a chats** – chats privados podem exigir permissões específicas.
- **Considerações de segurança** – mantenha `API_ID` e `API_HASH` em sigilo e não compartilhe o arquivo `.session`.
- **Uso responsável** – utilize a ferramenta apenas para o seu próprio backup, respeitando os termos do Telegram.
