# Documentação Completa - Telethon MTProto API

## Índice
1. [Introdução](#introdução)
2. [Login via QR Code](#login-via-qr-code)
3. [Exportar Lista de Chats/Grupos/Canais](#exportar-lista-de-chatsgruposcanais)
4. [Exportar Mídias de Forma Organizada](#exportar-mídias-de-forma-organizada)
5. [Funcionalidades Adicionais](#funcionalidades-adicionais)
6. [Exemplo Completo](#exemplo-completo)

---

## Introdução

A **MTProto API** do Telegram com a biblioteca **Telethon** oferece funcionalidades avançadas para automação e gerenciamento de dados. Esta documentação apresenta implementações completas para:

- Login via QR Code
- Exportação de listas de chats
- Download organizado de mídias
- Filtros avançados e controle de progresso

### Pré-requisitos

```bash
pip install telethon tqdm qrcode
```

### Configuração Inicial

```python
import telethon
from telethon import TelegramClient
from telethon.tl.functions.channels import GetForumTopicsRequest
from telethon.tl.types import Channel, PeerChannel, PeerChat
from qrcode import QRCode
import asyncio
import os
import json
from datetime import datetime, timedelta
from tqdm import tqdm

# Suas credenciais da MTProto API
api_id = 12345  # Substituir pelo seu API ID
api_hash = '0123456789abcdef0123456789abcdef'  # Substituir pelo seu API Hash
```

---

## Login via QR Code

O Telethon suporta autenticação via QR Code através do método `qr_login()`. Esta implementação permite login seguro sem necessidade de inserir número de telefone.

```python
qr = QRCode()

def gen_qr(token: str):
    """Gera QR Code no terminal"""
    qr.clear()
    qr.add_data(token)
    qr.print_ascii()

def display_url_as_qr(url):
    """Exibe URL e QR Code no terminal"""
    print(f"URL do QR Code: {url}")
    gen_qr(url)

async def login_with_qr():
    """
    Realiza login via QR Code com tratamento de erros
    Retorna cliente autenticado
    """
    client = TelegramClient("session_qr", api_id, api_hash)
    
    if not client.is_connected():
        await client.connect()
    
    qr_login = await client.qr_login()
    print("Cliente conectado:", client.is_connected())
    
    authenticated = False
    while not authenticated:
        display_url_as_qr(qr_login.url)
        print("Escaneie o QR Code com seu Telegram...")
        
        try:
            authenticated = await qr_login.wait(30)  # Timeout de 30 segundos
        except TimeoutError:
            print("QR Code expirou, gerando novo...")
            await qr_login.recreate()
        except Exception as e:
            if "SessionPasswordNeededError" in str(e):
                password = input("Digite sua senha 2FA: ")
                await client.sign_in(password=password)
                authenticated = True
    
    print("Login realizado com sucesso!")
    return client
```

**Características:**
- ✅ Suporte à autenticação 2FA
- ✅ Renovação automática de QR Code expirado
- ✅ Tratamento de erros robusto
- ✅ Sessão persistente

---

## Exportar Lista de Chats/Grupos/Canais

Esta função obtém uma lista completa de todos os chats, grupos e canais do usuário, salvando as informações em formato JSON.

```python
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

async def export_chat_list(client):
    """
    Exporta lista completa de chats, grupos e canais
    Salva em arquivo JSON com metadados detalhados
    """
    
    # Obter todos os diálogos
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=500,
        hash=0
    ))
    
    chat_list = []
    
    for chat in result.chats:
        chat_info = {
            'id': chat.id,
            'title': getattr(chat, 'title', 'N/A'),
            'username': getattr(chat, 'username', None),
            'type': chat.__class__.__name__,  # Chat, Channel, etc.
            'participants_count': getattr(chat, 'participants_count', 0),
            'date': getattr(chat, 'date', None),
            'access_hash': getattr(chat, 'access_hash', None)
        }
        chat_list.append(chat_info)
    
    # Salvar em arquivo JSON
    with open('chat_list.json', 'w', encoding='utf-8') as f:
        json.dump(chat_list, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Lista de {len(chat_list)} chats exportada para 'chat_list.json'")
    return chat_list
```

**Dados Exportados:**
- ID do chat
- Título/Nome
- Username (se disponível)
- Tipo (Chat, Channel, etc.)
- Número de participantes
- Data de criação
- Hash de acesso

---

## Exportar Mídias de Forma Organizada

Implementação completa para download organizado de mídias com criação automática de diretórios, organização cronológica e suporte a grupos com tópicos.

```python
from telethon.tl.functions.channels import GetForumTopicsRequest
from telethon.tl.types import Channel

async def get_forum_topics(client, chat_entity):
    """
    Obtém lista de tópicos de um grupo forum (se aplicável)
    Retorna dicionário com ID -> nome do tópico
    """
    topics = {}
    
    try:
        if isinstance(chat_entity, Channel) and getattr(chat_entity, 'forum', False):
            result = await client(GetForumTopicsRequest(
                channel=chat_entity,
                offset_date=None,
                offset_id=0,
                offset_topic=0,
                limit=100
            ))
            
            for topic in result.topics:
                if hasattr(topic, 'id') and hasattr(topic, 'title'):
                    topics[topic.id] = topic.title
                    
        return topics
    except Exception as e:
        print(f"Erro ao obter tópicos: {e}")
        return {}

def sanitize_filename(filename):
    """
    Remove caracteres inválidos do nome do arquivo/diretório
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

async def export_media_organized(client, chat_entity, limit=1000):
    """
    Exporta mídias de um chat de forma cronológica e organizada
    Suporte a grupos privados, públicos e com tópicos
    Cria estrutura de diretórios automaticamente
    """
    
    # Obter informações do chat
    chat_info = await client.get_entity(chat_entity)
    chat_name = getattr(chat_info, 'title', f'Chat_{chat_info.id}')
    chat_name_clean = sanitize_filename(chat_name)
    
    # Obter tópicos do forum (se aplicável)
    topics = await get_forum_topics(client, chat_info)
    is_forum = len(topics) > 0
    
    # Criar estrutura de diretórios base
    base_dir = f"exports/{chat_name_clean}_{chat_info.id}"
    
    def create_media_dirs(base_path, topic_name=None):
        """Cria estrutura de diretórios para mídias"""
        topic_suffix = f"/{sanitize_filename(topic_name)}" if topic_name else ""
        
        return {
            'photos': f"{base_path}{topic_suffix}/fotos",
            'videos': f"{base_path}{topic_suffix}/videos", 
            'documents': f"{base_path}{topic_suffix}/documentos",
            'audio': f"{base_path}{topic_suffix}/audio",
            'voice': f"{base_path}{topic_suffix}/mensagens_voz",
            'stickers': f"{base_path}{topic_suffix}/stickers",
            'other': f"{base_path}{topic_suffix}/outros"
        }
    
    # Diretórios principais (para mensagens sem tópico)
    main_media_dirs = create_media_dirs(base_dir)
    
    # Criar diretórios principais
    for dir_path in main_media_dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    
    # Diretórios por tópico (se for forum)
    topic_media_dirs = {}
    if is_forum:
        for topic_id, topic_name in topics.items():
            topic_dirs = create_media_dirs(base_dir, topic_name)
            topic_media_dirs[topic_id] = topic_dirs
            
            # Criar diretórios do tópico
            for dir_path in topic_dirs.values():
                os.makedirs(dir_path, exist_ok=True)
    
    # Arquivo de log para metadados
    log_file = f"{base_dir}/download_log.txt"
    
    downloaded_count = 0
    topic_counts = {}
    
    print(f"Iniciando download de mídias do chat: {chat_name}")
    if is_forum:
        print(f"Grupo com tópicos detectado. Tópicos encontrados: {len(topics)}")
        for topic_id, topic_name in topics.items():
            print(f"  - {topic_name} (ID: {topic_id})")
    
    async for message in tqdm(client.iter_messages(chat_entity, limit=limit), 
                             desc="Processando mensagens"):
        
        if message.media is None:
            continue
            
        try:
            # Determinar tópico da mensagem (se aplicável)
            topic_id = getattr(message, 'reply_to', None)
            topic_name = None
            current_dirs = main_media_dirs
            
            if topic_id and hasattr(topic_id, 'reply_to_top_id'):
                top_msg_id = topic_id.reply_to_top_id
                if top_msg_id in topics:
                    topic_name = topics[top_msg_id]
                    current_dirs = topic_media_dirs.get(top_msg_id, main_media_dirs)
                    
                    # Contar downloads por tópico
                    if topic_name not in topic_counts:
                        topic_counts[topic_name] = 0
            
            # Determinar tipo de mídia e diretório
            media_type = None
            target_dir = current_dirs['other']
            
            if message.photo:
                media_type = 'photo'
                target_dir = current_dirs['photos']
                extension = '.jpg'
            elif message.video:
                media_type = 'video'
                target_dir = current_dirs['videos']
                extension = '.mp4'
            elif message.voice:
                media_type = 'voice'
                target_dir = current_dirs['voice']
                extension = '.ogg'
            elif message.audio:
                media_type = 'audio'
                target_dir = current_dirs['audio']
                extension = '.mp3'
            elif message.sticker:
                media_type = 'sticker'
                target_dir = current_dirs['stickers']
                extension = '.webp'
            elif message.document:
                media_type = 'document'
                target_dir = current_dirs['documents']
                # Tentar obter extensão do arquivo
                if hasattr(message.document, 'attributes'):
                    for attr in message.document.attributes:
                        if hasattr(attr, 'file_name') and attr.file_name:
                            extension = os.path.splitext(attr.file_name)[1] or '.bin'
                            break
                    else:
                        extension = '.bin'
                else:
                    extension = '.bin'
            
            # Criar nome do arquivo com timestamp
            timestamp = message.date.strftime("%Y%m%d_%H%M%S")
            topic_prefix = f"[{sanitize_filename(topic_name)}]_" if topic_name else ""
            filename = f"{topic_prefix}{timestamp}_msg{message.id}{extension}"
            filepath = os.path.join(target_dir, filename)
            
            # Download do arquivo
            await client.download_media(message, file=filepath)
            
            # Log da operação
            with open(log_file, 'a', encoding='utf-8') as log:
                topic_info = f" - Tópico: {topic_name}" if topic_name else ""
                log.write(f"{datetime.now()}: {filename} - {media_type} - "
                         f"Msg ID: {message.id} - Data: {message.date}{topic_info}\n")
            
            downloaded_count += 1
            if topic_name:
                topic_counts[topic_name] += 1
            
        except Exception as e:
            print(f"Erro ao baixar mídia da mensagem {message.id}: {e}")
            continue
    
    # Relatório final
    print(f"Download concluído! {downloaded_count} arquivos baixados em {base_dir}")
    
    if topic_counts:
        print("Downloads por tópico:")
        for topic, count in topic_counts.items():
            print(f"  - {topic}: {count} arquivos")
    
    return downloaded_count

async def export_all_chats_media(client, chat_list, limit_per_chat=500):
    """
    Exporta mídias de múltiplos chats (públicos e privados)
    Processa lista de chats automaticamente
    Inclui verificação de permissões de acesso
    """
    
    successful_exports = 0
    failed_exports = 0
    
    for chat_info in chat_list:
        try:
            print(f"\nProcessando chat: {chat_info['title']} (ID: {chat_info['id']})")
            
            # Múltiplas tentativas de obter entidade do chat
            entity = None
            
            # Tentativa 1: Por username (se disponível)
            if chat_info.get('username'):
                try:
                    entity = await client.get_entity(chat_info['username'])
                    print(f"✅ Acesso via username: @{chat_info['username']}")
                except Exception as e:
                    print(f"⚠️ Falha no acesso via username: {e}")
            
            # Tentativa 2: Por ID direto
            if not entity:
                try:
                    entity = await client.get_entity(chat_info['id'])
                    print(f"✅ Acesso via ID: {chat_info['id']}")
                except Exception as e:
                    print(f"⚠️ Falha no acesso via ID: {e}")
            
            # Tentativa 3: Por access_hash (se disponível)
            if not entity and chat_info.get('access_hash'):
                try:
                    from telethon.tl.types import PeerChannel, PeerChat
                    
                    if chat_info['type'] == 'Channel':
                        peer = PeerChannel(chat_info['id'])
                    else:
                        peer = PeerChat(chat_info['id'])
                    
                    entity = await client.get_entity(peer)
                    print(f"✅ Acesso via peer com access_hash")
                except Exception as e:
                    print(f"⚠️ Falha no acesso via peer: {e}")
            
            if not entity:
                print(f"❌ Não foi possível acessar o chat: {chat_info['title']}")
                failed_exports += 1
                continue
            
            # Verificar se temos permissão para ver o histórico
            try:
                # Tentar obter uma mensagem para verificar acesso
                async for _ in client.iter_messages(entity, limit=1):
                    break
                print(f"✅ Permissão de leitura confirmada")
            except Exception as e:
                print(f"❌ Sem permissão para ler histórico: {e}")
                failed_exports += 1
                continue
            
            # Exportar mídias
            downloaded = await export_media_organized(client, entity, limit_per_chat)
            
            if downloaded > 0:
                successful_exports += 1
                print(f"✅ Concluído: {downloaded} arquivos baixados")
            else:
                print(f"ℹ️ Nenhuma mídia encontrada neste chat")
                
        except Exception as e:
            print(f"❌ Erro ao processar chat {chat_info['title']}: {e}")
            failed_exports += 1
            continue
    
    # Relatório final
    print(f"\n=== RELATÓRIO FINAL ===")
    print(f"Chats processados com sucesso: {successful_exports}")
    print(f"Chats com falha: {failed_exports}")
    print(f"Total de chats tentados: {len(chat_list)}")

```

**Estrutura de Diretórios Criada:**
```
exports/
└── ChatName_123456/
    ├── fotos/
    ├── videos/
    ├── documentos/
    ├── audio/
    ├── mensagens_voz/
    ├── stickers/
    ├── outros/
    ├── download_log.txt
    └── [PARA GRUPOS COM TÓPICOS]
        ├── NomeDoTopico1/
        │   ├── fotos/
        │   ├── videos/
        │   ├── documentos/
        │   ├── audio/
        │   ├── mensagens_voz/
        │   ├── stickers/
        │   └── outros/
        └── NomeDoTopico2/
            ├── fotos/
            ├── videos/
            ├── documentos/
            ├── audio/
            ├── mensagens_voz/
            ├── stickers/
            └── outros/
```

**Características:**
- ✅ Organização automática por tipo de mídia
- ✅ **Suporte a grupos com tópicos/fóruns** (subdiretórios automáticos)
- ✅ **Funciona com chats/grupos privados** que você faz parte
- ✅ Nomenclatura cronológica com timestamp
- ✅ **Prefixo do tópico** no nome dos arquivos
- ✅ Log detalhado de downloads (inclui informação do tópico)
- ✅ Tratamento de erros robusto com múltiplas tentativas de acesso
- ✅ Barra de progresso visual
- ✅ **Relatório de downloads por tópico**
- ✅ Sanitização de nomes de arquivos/diretórios

---

## Funcionalidades Adicionais

### Filtros por Data

```python
# Filtrar mensagens dos últimos 30 dias
start_date = datetime.now() - timedelta(days=30)

async for message in client.iter_messages(chat_entity, offset_date=start_date):
    # Processar apenas mensagens recentes
    pass

# Filtrar por período específico
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

async for message in client.iter_messages(chat_entity, 
                                        offset_date=end_date, 
                                        reverse=True):
    if message.date < start_date:
        break
    # Processar mensagem
```

### Filtros por Tipo de Arquivo

```python
async def download_specific_media_type(client, chat_entity, media_types=['photo']):
    """
    Download apenas tipos específicos de mídia
    media_types: ['photo', 'video', 'document', 'audio', 'voice', 'sticker']
    """
    
    async for message in client.iter_messages(chat_entity):
        if message.media is None:
            continue
            
        should_download = False
        
        if 'photo' in media_types and message.photo:
            should_download = True
        elif 'video' in media_types and message.video:
            should_download = True
        elif 'document' in media_types and message.document:
            should_download = True
        elif 'audio' in media_types and message.audio:
            should_download = True
        elif 'voice' in media_types and message.voice:
            should_download = True
        elif 'sticker' in media_types and message.sticker:
            should_download = True
            
        if should_download:
            await client.download_media(message)
```

### Funcionalidades Específicas para Tópicos

```python
async def download_specific_topic(client, chat_entity, topic_name, limit=1000):
    """
    Download de mídias de um tópico específico
    """
    
    # Obter tópicos do chat
    topics = await get_forum_topics(client, chat_entity)
    
    # Encontrar ID do tópico pelo nome
    topic_id = None
    for tid, tname in topics.items():
        if tname.lower() == topic_name.lower():
            topic_id = tid
            break
    
    if not topic_id:
        print(f"Tópico '{topic_name}' não encontrado")
        return 0
    
    print(f"Baixando mídias do tópico: {topic_name}")
    
    count = 0
    async for message in client.iter_messages(chat_entity, limit=limit):
        # Verificar se a mensagem pertence ao tópico
        if (hasattr(message, 'reply_to') and 
            hasattr(message.reply_to, 'reply_to_top_id') and
            message.reply_to.reply_to_top_id == topic_id):
            
            if message.media:
                await client.download_media(message)
                count += 1
    
    print(f"Download concluído: {count} arquivos do tópico '{topic_name}'")
    return count

async def list_forum_topics(client, chat_entity):
    """
    Lista todos os tópicos de um grupo forum
    """
    
    topics = await get_forum_topics(client, chat_entity)
    
    if not topics:
        print("Este chat não possui tópicos ou não é um grupo forum")
        return
    
    print(f"Tópicos encontrados ({len(topics)}):")
    for topic_id, topic_name in topics.items():
        print(f"  ID: {topic_id} - Nome: {topic_name}")
    
    return topics
```

---

## Exemplo Completo

Implementação completa que utiliza todas as funcionalidades:

```python
async def main():
    """
    Função principal que executa todo o processo:
    1. Login via QR Code
    2. Exportação da lista de chats
    3. Download organizado de mídias
    """
    
    try:
        # 1. Login via QR Code
        print("=== INICIANDO LOGIN VIA QR CODE ===")
        client = await login_with_qr()
        
        # 2. Exportar lista de chats
        print("\n=== EXPORTANDO LISTA DE CHATS ===")
        chat_list = await export_chat_list(client)
        
        # 3. Mostrar chats encontrados
        print(f"\nChats encontrados ({len(chat_list)}):")
        for i, chat in enumerate(chat_list[:10]):  # Mostrar apenas os primeiros 10
            print(f"{i+1}. {chat['title']} ({chat['type']}) - {chat['participants_count']} membros")
        
        # 4. Exportar mídias dos primeiros 5 chats
        print("\n=== INICIANDO DOWNLOAD DE MÍDIAS ===")
        await export_all_chats_media(client, chat_list[:5], limit_per_chat=100)
        
        print("\n=== PROCESSO CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        print(f"Erro durante execução: {e}")
    
    finally:
        # Desconectar cliente
        if 'client' in locals():
            await client.disconnect()
            print("Cliente desconectado.")

# Executar o programa principal
if __name__ == "__main__":
    asyncio.run(main())
```

### Script de Execução Simples

```python
# arquivo: telegram_export.py
import asyncio
from telegram_functions import *  # Importar todas as funções

# Configurar suas credenciais
api_id = 12345
api_hash = 'sua_api_hash_aqui'

# Executar
asyncio.run(main())
```

---

## Notas Importantes

### Configuração da API
1. Acesse [my.telegram.org](https://my.telegram.org)
2. Faça login com seu número de telefone
3. Vá em "API Development Tools"
4. Crie uma nova aplicação
5. Anote seu `api_id` e `api_hash`

### Limitações e Considerações
- **Rate Limits**: O Telegram impõe limites de requisições
- **Tamanho de Arquivos**: Arquivos grandes podem demorar para baixar
- **Permissões**: Alguns chats podem ter restrições de acesso
- **Armazenamento**: Considere o espaço em disco disponível

### Tratamento de Erros Comuns
- **FloodWaitError**: Aguarde o tempo especificado
- **ChatAdminRequiredError**: Você precisa ser admin do chat
- **ChannelPrivateError**: Chat privado ou não acessível

### Boas Práticas
- ✅ Sempre use `try/except` para tratamento de erros
- ✅ Implemente delays entre downloads massivos
- ✅ Monitore o uso de memória para chats grandes
- ✅ Faça backup regular dos arquivos de sessão
- ✅ Respeite os termos de uso do Telegram

---

*Esta documentação fornece uma base sólida para automação do Telegram usando Telethon. Adapte as funções conforme suas necessidades específicas.*