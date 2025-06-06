# 📱 Telegram Media Downloader

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-Latest-green.svg)](https://docs.telethon.dev)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#-licença)
[![Status](https://img.shields.io/badge/Status-MVP%20v1.0-brightgreen.svg)](#-funcionalidades)

**Ferramenta automatizada para download organizado de mídias do Telegram**  
*Utilizando MTProto API através da biblioteca Telethon*

[🚀 Instalação Rápida](#-instalação-rápida) • [📖 Guia de Uso](#-guia-de-uso) • [🔧 Configuração](#-configuração) • [🐛 Problemas?](#-solução-de-problemas)

</div>

---

## 🎯 Por que usar?

> **Backup completo e organizado das suas conversas do Telegram de forma automatizada**

- 🔐 **Login seguro** via QR Code (sem compartilhar número)
- 📁 **Organização automática** por tipo de mídia e tópicos
- 🚀 **Interface intuitiva** com progresso visual
- 📊 **Logs detalhados** de todo o processo
- 🔒 **Acesso inteligente** a chats privados com fallbacks

## ✨ Funcionalidades

<table>
<tr>
<td width="50%">

### 🔥 Recursos Principais
- [x] Login via QR Code
- [x] Exportação de lista de chats
- [x] Download organizado por categoria
- [x] Suporte a grupos com tópicos
- [x] Múltiplas tentativas de acesso
- [x] Logs e progresso visual

</td>
<td width="50%">

### 🛠️ Tecnologias
- [x] Autenticação 2FA
- [x] Sessão persistente
- [x] Tratamento robusto de erros
- [x] Nomenclatura cronológica
- [x] Sanitização automática
- [x] Barra de progresso (tqdm)

</td>
</tr>
</table>

## 🚀 Instalação Rápida

### Pré-requisitos
```bash
Python 3.8+ • Conta Telegram • API Credentials
```

### 1️⃣ Obter credenciais API
<details>
<summary>📝 <strong>Clique para ver o passo a passo</strong></summary>

1. Acesse [my.telegram.org/apps](https://my.telegram.org/apps)
2. Faça login com seu número do Telegram
3. Vá em **"API Development Tools"**
4. Crie uma nova aplicação
5. Anote seu `api_id` e `api_hash`

</details>

### 2️⃣ Configurar projeto
```bash
# Clonar repositório
git clone <repository-url>
cd telegram-media-downloader

# Instalar dependências
pip install -r requirements.txt

# Configurar credenciais
# Copie o arquivo `.env.example` para `.env` e edite com seus valores:
cp .env.example .env
API_ID=12345
API_HASH='sua_api_hash_aqui'
```

### 3️⃣ Executar
```bash
python telegram_downloader.py
```

### Quickstart (English)

```bash
cp .env.example .env  # configure your Telegram API credentials
pip install -r requirements.txt
python telegram_downloader.py --limit 500
```

## 📖 Guia de Uso

### 🔄 Fluxo Completo

```mermaid
graph LR
    A[Executar Script] --> B[Escanear QR Code]
    B --> C[Lista de Chats]
    C --> D[Selecionar Chats]
    D --> E[Download Automático]
    E --> F[Arquivos Organizados]
```

### 📱 Métodos de Seleção

<table>
<tr>
<th>Método</th>
<th>Exemplo</th>
<th>Descrição</th>
</tr>
<tr>
<td>🆔 Por ID</td>
<td><code>123456789</code></td>
<td>ID único do chat</td>
</tr>
<tr>
<td>🔗 Por Link</td>
<td><code>https://t.me/username</code></td>
<td>Link público ou privado</td>
</tr>
<tr>
<td>@ Username</td>
<td><code>@username</code></td>
<td>Username com ou sem @</td>
</tr>
<tr>
<td>📋 Da Lista</td>
<td><code>1,3-5,8</code></td>
<td>Seleção múltipla da lista</td>
</tr>
</table>

### 📁 Estrutura de Saída

```
exports/
├── 📋 chat_list.json                    # Lista completa de chats
└── 📁 {ChatName}_{ChatID}/
    ├── 📸 fotos/                        # Imagens (.jpg, .png)
    ├── 🎥 videos/                       # Vídeos (.mp4, .avi)
    ├── 📄 documentos/                   # PDFs, documentos
    ├── 🎵 audio/                        # Músicas (.mp3)
    ├── 🎤 mensagens_voz/               # Voice messages (.ogg)
    ├── 😊 stickers/                    # Stickers (.webp)
    ├── 📦 outros/                      # Outros tipos
    ├── 📊 download_log.txt             # Log detalhado
    └── 🗂️ [GRUPOS COM TÓPICOS]/
        ├── TopicName1/
        └── TopicName2/
```

## 🔧 Configuração

### ⚙️ Arquivo `config.py`

```python
# 📊 Limites e Performance
DEFAULT_LIMIT_PER_CHAT = 1000        # Mensagens por chat
MAX_FILE_SIZE = 1024 * 1024 * 1024   # Limite: 1GB por arquivo
CONCURRENT_DOWNLOADS = 1              # Downloads simultâneos

# 📱 Tipos de mídia suportados
SUPPORTED_MEDIA_TYPES = [
    'photo', 'video', 'document', 'audio', 'voice', 'sticker'
]
```

### 🎨 Personalização

<details>
<summary><strong>🔧 Opções Avançadas</strong></summary>

| Configuração | Arquivo | Função |
|-------------|---------|---------|
| **Limite de mensagens** | `config.py` | `DEFAULT_LIMIT_PER_CHAT` |
| **Seleção de chats** | `telegram_downloader.py` | `interactive_chat_selection()` |
| **Filtros personalizados** | `telethon_handlers.py` | Adicionar filtros |
| **Estrutura de pastas** | `config.py` | `MEDIA_DIRECTORIES` |

</details>

## 📊 Exemplo de Execução

```bash
╔══════════════════════════════════════════════════════════════╗
║                  TELEGRAM MEDIA DOWNLOADER                  ║
║                         MVP v1.0                            ║
╠══════════════════════════════════════════════════════════════╣
║  📱 Login via QR Code          📋 Export Chat Lists         ║
║  📥 Organized Downloads        📁 Forum Topics Support      ║
║  🔒 Private Chats Access       📊 Detailed Logging          ║
╚══════════════════════════════════════════════════════════════╝

🔐 ETAPA 1: AUTENTICAÇÃO
📱 Escaneie o QR Code com seu Telegram...
✅ Login realizado com sucesso!

📋 ETAPA 2: EXPORTAÇÃO (25 chats encontrados)
📊 Canais: 8 • Grupos: 12 • Privados: 5

📥 ETAPA 3: DOWNLOAD
📱 Processando: Meu Grupo Favorito (1/5)
📁 Forum detectado - 3 tópicos encontrados
📥 [████████████████████] 45/45 arquivos

✅ CONCLUÍDO!
📊 Estatísticas finais:
   • 150 mensagens processadas
   • 45 arquivos baixados
   • 3 tópicos organizados
```

## 🛡️ Segurança & Limitações

### ✅ Boas Práticas Implementadas

- 🔒 **Segurança**: Apenas chats acessíveis ao usuário
- 🔐 **Privacidade**: Sessões criptografadas localmente
- ⚡ **Rate Limiting**: Respeita limites do Telegram
- 🛠️ **Robustez**: Tratamento completo de erros

### ⚠️ Limitações Conhecidas

| Limitação | Impacto | Solução |
|-----------|---------|---------|
| Rate limits do Telegram | Delays automáticos | Aguarda tempo especificado |
| Arquivos muito grandes | Download lento | Configurable em `MAX_FILE_SIZE` |
| Chats privados restritos | Alguns inacessíveis | Múltiplas tentativas automáticas |
| Espaço em disco | Pode esgotar | Monitore espaço disponível |

## 🐛 Solução de Problemas

<details>
<summary><strong>❌ Erro de autenticação</strong></summary>

**Problema**: `AuthKeyError` ou `ApiIdInvalidError`

**Solução**:
```python
# Verifique o arquivo `.env`
API_ID=12345  # Deve ser um número
API_HASH='hash_correto'  # String válida do Telegram
```
</details>

<details>
<summary><strong>❌ QR Code não aparece</strong></summary>

**Problema**: Terminal não exibe QR Code

**Solução**:
```bash
pip install qrcode[pil]
# Ou usar terminal com suporte Unicode
```
</details>

<details>
<summary><strong>❌ Sem permissão para chat</strong></summary>

**Problema**: `ChatAdminRequiredError`

**Solução**: Normal - app continua automaticamente com próximos chats
</details>

<details>
<summary><strong>❌ Erro de memória</strong></summary>

**Problema**: `MemoryError` com muitos arquivos

**Solução**:
```python
# Reduza em config.py
DEFAULT_LIMIT_PER_CHAT = 100  # Valor menor
```
</details>

### 📋 Logs e Debug

- 📊 **Logs detalhados**: `exports/{chat}/download_log.txt`
- 🎨 **Erros coloridos**: Terminal com códigos de cor
- 🔍 **Debug personalizado**: Adicione `print()` conforme necessário

## 🗂️ Estrutura do Projeto

```
telegram-media-downloader/
├── 📄 README.md                 # Esta documentação
├── ⚙️ config.py                 # Configurações centrais
├── 🔧 file_utils.py             # Utilitários de arquivo
├── 📡 telethon_handlers.py      # Core Telethon
├── 🚀 telegram_downloader.py    # Script principal
└── 📦 requirements.txt          # Dependências
```

## 🖥️ API e Docker

O projeto pode ser executado como uma API HTTP utilizando **FastAPI**.
Um arquivo `Dockerfile` e um `docker-compose.yml` já estão disponíveis para
facilitar a implantação em ambientes com Traefik.

1. Construa e inicie o container:

```bash
docker compose up -d
```

2. A API ficará acessível em `https://telegram.zebook.tech` quando a regra do
Traefik estiver ativa.

Os endpoints estão documentados em [`docs/API_ENDPOINTS.md`](docs/API_ENDPOINTS.md).

## 🚀 Roadmap

### 📅 Fase 2 - Recursos Avançados
- [ ] 📅 Filtros por data e tamanho
- [ ] 🖥️ Interface gráfica opcional  
- [ ] 🔄 Sincronização incremental
- [ ] ☁️ Backup em nuvem
- [ ] 👤 Filtros por usuário

### 📅 Fase 3 - Performance
- [ ] ⚡ Downloads paralelos seguros
- [ ] 📦 Compressão automática
- [ ] ▶️ Retomada de downloads
- [ ] 📊 Dashboard web

## 📄 Licença

<div align="center">

**Projeto educacional fornecido "como está"**  
*Use responsavelmente e respeite os termos do Telegram*

</div>

## 🤝 Contribuindo

Contribuições são muito bem-vindas! 

- 🐛 **Reportar bugs** via Issues
- 💡 **Sugerir features** via Discussions  
- 🔧 **Pull requests** sempre aceitos
- 📖 **Melhorar docs** é sempre útil

## ⚠️ Aviso Legal

> **⚖️ Use apenas para backup pessoal**
> - ✅ Suas próprias conversas
> - ❌ Não redistribua conteúdo de terceiros
> - 📜 Respeite termos de uso do Telegram
> - 🔒 Mantenha privacidade de outros usuários

---

<div align="center">

**📱 Telegram Media Downloader v1.0**  
*Desenvolvido com ❤️ para a comunidade*

[⬆️ Voltar ao topo](#-telegram-media-downloader)

</div>
