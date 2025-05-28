
"""
Telethon handlers module for Telegram Media Downloader
Contains all Telethon-specific functionality including authentication,
chat listing, media downloading, and forum topic handling
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from telethon import TelegramClient
from telethon.tl.functions.channels import GetForumTopicsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import Channel, InputPeerEmpty
from qrcode import QRCode
from tqdm import tqdm

from config import API_ID, API_HASH, SESSION_NAME, EXPORTS_DIR
from file_utils import (
    sanitize_filename, create_media_directories, ensure_directories_exist,
    get_media_type_name, generate_filename, write_download_log, format_file_size
)


def generate_qr_code(token: str) -> None:
    """Generate and display QR code in terminal"""
    qr = QRCode()
    qr.clear()
    qr.add_data(token)
    qr.print_ascii()


def display_url_as_qr(url: str) -> None:
    """Display URL and QR code in terminal"""
    print(f"URL do QR Code: {url}")
    generate_qr_code(url)


async def login_with_qr() -> TelegramClient:
    """
    Perform QR code login with error handling
    
    Returns:
        Authenticated Telegram client
    """
    print("=== INICIANDO LOGIN VIA QR CODE ===")
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    if not client.is_connected():
        await client.connect()
    
    # Check if already authenticated
    if await client.is_user_authorized():
        print("✅ Sessão existente encontrada - Login automático realizado!")
        return client
    
    print("🔐 Iniciando processo de autenticação via QR Code...")
    qr_login = await client.qr_login()
    print("📱 Cliente conectado:", client.is_connected())
    
    authenticated = False
    attempt = 1
    
    while not authenticated:
        print(f"\n--- Tentativa {attempt} ---")
        display_url_as_qr(qr_login.url)
        print("📱 Escaneie o QR Code com seu Telegram...")
        print("⏱️  Aguardando 30 segundos...")
        
        try:
            authenticated = await qr_login.wait(30)  # 30 second timeout
            if authenticated:
                print("✅ Login realizado com sucesso!")
            
        except TimeoutError:
            print("⏰ QR Code expirou, gerando novo...")
            await qr_login.recreate()
            attempt += 1
            
        except Exception as e:
            error_str = str(e)
            if "SessionPasswordNeededError" in error_str:
                print("🔐 Autenticação 2FA necessária")
                password = input("Digite sua senha 2FA: ")
                try:
                    await client.sign_in(password=password)
                    authenticated = True
                    print("✅ Login com 2FA realizado com sucesso!")
                except Exception as auth_error:
                    print(f"❌ Erro na autenticação 2FA: {auth_error}")
                    return None
            else:
                print(f"❌ Erro durante login: {e}")
                attempt += 1
                if attempt > 5:
                    print("❌ Muitas tentativas falhas. Encerrando...")
                    return None
    
    print("🎉 Autenticação concluída com sucesso!")
    return client


async def export_chat_list(client: TelegramClient) -> List[Dict]:
    """
    Export complete list of chats, groups and channels
    
    Args:
        client: Authenticated Telegram client
        
    Returns:
        List of chat information dictionaries
    """
    print("📋 Exportando lista de chats...")
    
    try:
        # Get all dialogs
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
                'title': getattr(chat, 'title', f'Chat_{chat.id}'),
                'username': getattr(chat, 'username', None),
                'type': chat.__class__.__name__,
                'participants_count': getattr(chat, 'participants_count', 0),
                'date': getattr(chat, 'date', None),
                'access_hash': getattr(chat, 'access_hash', None),
                'is_forum': getattr(chat, 'forum', False)
            }
            chat_list.append(chat_info)
        
        # Save to JSON file
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        json_path = os.path.join(EXPORTS_DIR, 'chat_list.json')
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(chat_list, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Lista de {len(chat_list)} chats exportada para '{json_path}'")
        return chat_list
        
    except Exception as e:
        print(f"❌ Erro ao exportar lista de chats: {e}")
        return []


async def get_forum_topics(client: TelegramClient, chat_entity) -> Dict[int, str]:
    """
    Get forum topics from a forum group
    
    Args:
        client: Telegram client
        chat_entity: Chat entity object
        
    Returns:
        Dictionary mapping topic ID to topic name
    """
    topics = {}
    
    try:
        if isinstance(chat_entity, Channel) and getattr(chat_entity, 'forum', False):
            print("📁 Detectado grupo forum - obtendo tópicos...")
            
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
            
            print(f"📁 Encontrados {len(topics)} tópicos no grupo forum")
            for topic_id, topic_name in topics.items():
                print(f"   - {topic_name} (ID: {topic_id})")
                    
        return topics
        
    except Exception as e:
        print(f"⚠️ Erro ao obter tópicos: {e}")
        return {}


async def export_media_organized(client: TelegramClient, chat_entity, 
                                limit: int = 1000) -> int:
    """
    Export media from a chat in organized structure
    
    Args:
        client: Telegram client
        chat_entity: Chat entity to download from
        limit: Maximum number of messages to process
        
    Returns:
        Number of files downloaded
    """
    # Get chat information
    chat_info = await client.get_entity(chat_entity)
    chat_name = getattr(chat_info, 'title', f'Chat_{chat_info.id}')
    chat_name_clean = sanitize_filename(chat_name)
    
    print(f"📥 Iniciando download de mídias do chat: {chat_name}")
    
    # Get forum topics if applicable
    topics = await get_forum_topics(client, chat_info)
    is_forum = len(topics) > 0
    
    # Create base directory structure
    base_dir = os.path.join(EXPORTS_DIR, f"{chat_name_clean}_{chat_info.id}")
    
    # Main media directories (for messages without topics)
    main_media_dirs = create_media_directories(base_dir)
    ensure_directories_exist(main_media_dirs)
    
    # Topic-specific directories (if forum)
    topic_media_dirs = {}
    if is_forum:
        for topic_id, topic_name in topics.items():
            topic_dirs = create_media_directories(base_dir, topic_name)
            topic_media_dirs[topic_id] = topic_dirs
            ensure_directories_exist(topic_dirs)
    
    # Setup logging
    log_file = os.path.join(base_dir, "download_log.txt")
    
    # Counters
    downloaded_count = 0
    topic_counts = {}
    processed_count = 0
    
    print(f"📁 Estrutura de diretórios criada em: {base_dir}")
    if is_forum:
        print(f"📂 Grupo com tópicos detectado - {len(topics)} tópicos organizados")
    
    # Process messages with progress bar
    print("🔄 Processando mensagens...")
    
    # Initialize progress bar manually for async iteration
    pbar = tqdm(total=limit, desc="Analisando mensagens", unit="msg")
    
    async for message in client.iter_messages(chat_entity, limit=limit):
        processed_count += 1
        pbar.update(1)
        
        # Skip messages without media
        if message.media is None:
            continue
            
        try:
            # Determine message topic (if applicable)
            topic_id = None
            topic_name = None
            current_dirs = main_media_dirs
            
            if (is_forum and hasattr(message, 'reply_to') and 
                message.reply_to and hasattr(message.reply_to, 'reply_to_top_id')):
                
                top_msg_id = message.reply_to.reply_to_top_id
                if top_msg_id in topics:
                    topic_id = top_msg_id
                    topic_name = topics[top_msg_id]
                    current_dirs = topic_media_dirs.get(top_msg_id, main_media_dirs)
                    
                    # Initialize topic counter
                    if topic_name not in topic_counts:
                        topic_counts[topic_name] = 0
            
            # Determine media type and target directory
            media_type = get_media_type_name(message)
            target_dir = current_dirs.get(media_type, current_dirs['other'])
            
            # Generate filename
            filename = generate_filename(message, topic_name)
            filepath = os.path.join(target_dir, filename)
            
            # Download the file
            print(f"📥 Baixando: {filename}")
            await client.download_media(message, file=filepath)
            
            # Log the operation
            write_download_log(log_file, filename, media_type, 
                             message.id, message.date, topic_name)
            
            downloaded_count += 1
            if topic_name:
                topic_counts[topic_name] += 1
                
        except Exception as e:
            print(f"❌ Erro ao baixar mídia da mensagem {message.id}: {e}")
            continue
    
    # Close progress bar
    pbar.close()
    
    # Final report
    print(f"\n✅ Download concluído!")
    print(f"📊 Estatísticas:")
    print(f"   - Mensagens processadas: {processed_count}")
    print(f"   - Arquivos baixados: {downloaded_count}")
    print(f"   - Diretório: {base_dir}")
    
    if topic_counts:
        print(f"📁 Downloads por tópico:")
        for topic, count in topic_counts.items():
            print(f"   - {topic}: {count} arquivos")
    
    return downloaded_count


async def export_all_chats_media(client: TelegramClient, chat_list: List[Dict], 
                                limit_per_chat: int = 500) -> Tuple[int, int]:
    """
    Export media from multiple chats
    
    Args:
        client: Telegram client
        chat_list: List of chat information dictionaries
        limit_per_chat: Message limit per chat
        
    Returns:
        Tuple of (successful_exports, failed_exports)
    """
    successful_exports = 0
    failed_exports = 0
    
    print(f"🚀 Iniciando exportação de {len(chat_list)} chats...")
    
    for i, chat_info in enumerate(chat_list, 1):
        print(f"\n{'='*60}")
        print(f"📱 Processando chat {i}/{len(chat_list)}: {chat_info['title']}")
        print(f"   ID: {chat_info['id']} | Tipo: {chat_info['type']}")
        
        try:
            # Get entity using improved resolution
            entity = await get_chat_entity_safe(client, chat_info)
            
            if not entity:
                print(f"❌ Não foi possível acessar o chat: {chat_info['title']}")
                failed_exports += 1
                continue
            
            # Check read permissions
            try:
                async for _ in client.iter_messages(entity, limit=1):
                    break
                print(f"✅ Permissão de leitura confirmada")
            except Exception as e:
                print(f"❌ Sem permissão para ler histórico: {e}")
                failed_exports += 1
                continue
            
            # Export media
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
    
    return successful_exports, failed_exports


async def get_chat_entity_safe(client: TelegramClient, chat_info: Dict):
    """
    Safely get chat entity with multiple fallback methods
    
    Args:
        client: Telegram client
        chat_info: Chat information dictionary
        
    Returns:
        Chat entity or None if failed
    """
    entity = None
    chat_title = chat_info.get('title', 'Unknown')
    
    print(f"🔍 Tentando acessar chat: {chat_title}")
    
    # Method 1: Try username first (most reliable for public chats)
    if chat_info.get('username'):
        try:
            print(f"   📝 Tentativa 1: Username @{chat_info['username']}")
            entity = await client.get_entity(chat_info['username'])
            print(f"   ✅ Sucesso via username")
            return entity
        except Exception as e:
            print(f"   ❌ Falha via username: {e}")
    
    # Method 2: Try by ID
    if chat_info.get('id') and chat_info['id'] != 0:
        try:
            print(f"   🆔 Tentativa 2: ID {chat_info['id']}")
            entity = await client.get_entity(chat_info['id'])
            print(f"   ✅ Sucesso via ID")
            return entity
        except Exception as e:
            print(f"   ❌ Falha via ID: {e}")
    
    # Method 3: Try with access_hash if available
    if chat_info.get('access_hash'):
        try:
            print(f"   🔑 Tentativa 3: ID + access_hash")
            from telethon.tl.types import PeerChannel, PeerChat, PeerUser
            
            chat_id = chat_info['id']
            if chat_id < 0:
                if str(chat_id).startswith('-100'):
                    # Channel/Supergroup
                    peer = PeerChannel(int(str(chat_id)[4:]))
                else:
                    # Legacy group
                    peer = PeerChat(-chat_id)
            else:
                # User
                peer = PeerUser(chat_id)
            
            entity = await client.get_entity(peer)
            print(f"   ✅ Sucesso via access_hash")
            return entity
        except Exception as e:
            print(f"   ❌ Falha via access_hash: {e}")
    
    # Method 4: Try resolving username without @ prefix
    if chat_info.get('username'):
        try:
            username_clean = chat_info['username'].lstrip('@')
            print(f"   📝 Tentativa 4: Username limpo '{username_clean}'")
            entity = await client.get_entity(username_clean)
            print(f"   ✅ Sucesso via username limpo")
            return entity
        except Exception as e:
            print(f"   ❌ Falha via username limpo: {e}")
    
    print(f"   ❌ Todas as tentativas falharam para: {chat_title}")
    return None


async def validate_chat_access(client: TelegramClient, entity) -> bool:
    """
    Validate if we have read access to a chat
    
    Args:
        client: Telegram client
        entity: Chat entity
        
    Returns:
        True if access is available, False otherwise
    """
    try:
        async for _ in client.iter_messages(entity, limit=1):
            return True
    except:
        return False
    
    return False
