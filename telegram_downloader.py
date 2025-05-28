
"""
Telegram Media Downloader - Main Application
Automated tool for downloading and organizing media from Telegram chats

This is the main entry point that orchestrates the entire download process
following the MVP specifications from the PRD.
"""

import asyncio
import sys
from typing import List, Dict

from config import DEFAULT_LIMIT_PER_CHAT
from telethon_handlers import (
    login_with_qr, export_chat_list, export_all_chats_media
)


def print_banner():
    """Display application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  TELEGRAM MEDIA DOWNLOADER                  ║
║                         MVP v1.0                            ║
╠══════════════════════════════════════════════════════════════╣
║  📱 Login via QR Code                                        ║
║  📋 Export Chat Lists                                        ║
║  📥 Organized Media Downloads                                ║
║  📁 Forum Topics Support                                     ║
║  🔒 Private Chats Access                                     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_usage_instructions():
    """Display usage instructions"""
    instructions = """
📖 INSTRUÇÕES DE USO:

1. Configure suas credenciais da API no arquivo config.py:
   - API_ID: Seu ID da API do Telegram
   - API_HASH: Seu hash da API do Telegram
   - Obtenha em: https://my.telegram.org/apps

2. Execute o aplicativo:
   python telegram_downloader.py

3. Escaneie o QR Code que aparecerá no terminal

4. Aguarde o processo de exportação automática

📁 ESTRUTURA DE SAÍDA:
exports/
├── chat_list.json (lista de todos os chats)
└── {ChatName}_{ChatID}/
    ├── fotos/
    ├── videos/
    ├── documentos/
    ├── audio/
    ├── mensagens_voz/
    ├── stickers/
    ├── outros/
    └── download_log.txt

Para grupos com tópicos, subdiretórios serão criados automaticamente.
    """
    print(instructions)


def display_chat_summary(chat_list: List[Dict]) -> None:
    """
    Display summary of found chats
    
    Args:
        chat_list: List of chat information dictionaries
    """
    if not chat_list:
        print("❌ Nenhum chat encontrado")
        return
    
    print(f"\n📋 RESUMO DOS CHATS ENCONTRADOS ({len(chat_list)} total):")
    print("-" * 80)
    
    # Group by type
    by_type = {}
    for chat in chat_list:
        chat_type = chat['type']
        if chat_type not in by_type:
            by_type[chat_type] = []
        by_type[chat_type].append(chat)
    
    # Display summary by type
    for chat_type, chats in by_type.items():
        print(f"📂 {chat_type}: {len(chats)} chats")
    
    print("-" * 80)
    
    # Show first 10 chats as examples
    print("🔍 Primeiros 10 chats (exemplo):")
    for i, chat in enumerate(chat_list[:10], 1):
        forum_indicator = " 📁[FORUM]" if chat.get('is_forum') else ""
        participants = chat.get('participants_count', 0)
        print(f"{i:2d}. {chat['title'][:50]:<50} | {chat['type']:<10} | "
              f"{participants:>6} membros{forum_indicator}")
    
    if len(chat_list) > 10:
        print(f"    ... e mais {len(chat_list) - 10} chats")


async def interactive_chat_selection(chat_list: List[Dict]) -> List[Dict]:
    """
    Allow user to interactively select which chats to process
    For MVP, we'll process a limited number automatically
    
    Args:
        chat_list: List of all available chats
        
    Returns:
        List of selected chats to process
    """
    print(f"\n🎯 SELEÇÃO DE CHATS PARA DOWNLOAD")
    print("Para este MVP, vamos processar os primeiros 5 chats automaticamente.")
    print("Você pode modificar esta lógica no código conforme necessário.")
    
    # For MVP, automatically select first 5 chats
    selected_chats = chat_list[:5]
    
    print(f"\n📌 Chats selecionados para download ({len(selected_chats)}):")
    for i, chat in enumerate(selected_chats, 1):
        forum_indicator = " 📁[FORUM]" if chat.get('is_forum') else ""
        print(f"{i}. {chat['title']}{forum_indicator}")
    
    # Ask for confirmation
    confirmation = input("\n❓ Continuar com estes chats? (s/N): ").lower().strip()
    
    if confirmation in ['s', 'sim', 'y', 'yes']:
        return selected_chats
    else:
        print("❌ Operação cancelada pelo usuário")
        return []


async def main():
    """
    Main application function that orchestrates the entire process:
    1. QR Code Login
    2. Chat List Export
    3. Organized Media Download
    """
    print_banner()
    
    try:
        # Step 1: Authentication via QR Code
        print("🔐 ETAPA 1: AUTENTICAÇÃO")
        client = await login_with_qr()
        
        if not client:
            print("❌ Falha na autenticação. Encerrando aplicação.")
            return
        
        # Step 2: Export chat list
        print("\n📋 ETAPA 2: EXPORTAÇÃO DA LISTA DE CHATS")
        chat_list = await export_chat_list(client)
        
        if not chat_list:
            print("❌ Não foi possível obter lista de chats")
            await client.disconnect()
            return
        
        # Step 3: Display chat summary
        display_chat_summary(chat_list)
        
        # Step 4: Chat selection (for MVP, automatic selection)
        print("\n🎯 ETAPA 3: SELEÇÃO DE CHATS")
        selected_chats = await interactive_chat_selection(chat_list)
        
        if not selected_chats:
            print("ℹ️ Nenhum chat selecionado para download")
            await client.disconnect()
            return
        
        # Step 5: Media download
        print("\n📥 ETAPA 4: DOWNLOAD DE MÍDIAS")
        print(f"🎯 Limite de mensagens por chat: {DEFAULT_LIMIT_PER_CHAT}")
        
        successful, failed = await export_all_chats_media(
            client, selected_chats, DEFAULT_LIMIT_PER_CHAT
        )
        
        # Final report
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL")
        print("="*60)
        print(f"✅ Chats processados com sucesso: {successful}")
        print(f"❌ Chats com falha: {failed}")
        print(f"📊 Total de chats tentados: {len(selected_chats)}")
        print(f"📁 Arquivos salvos no diretório: exports/")
        
        if successful > 0:
            print("\n🎉 DOWNLOAD CONCLUÍDO COM SUCESSO!")
            print("📁 Verifique o diretório 'exports/' para seus arquivos")
        else:
            print("\n⚠️ Nenhum chat foi processado com sucesso")
            
    except KeyboardInterrupt:
        print("\n\n❌ Operação interrompida pelo usuário")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("💡 Dica: Verifique suas credenciais da API no arquivo config.py")
        
    finally:
        # Always disconnect client
        if 'client' in locals() and client:
            await client.disconnect()
            print("🔌 Cliente desconectado")
        
        print("\n👋 Obrigado por usar o Telegram Media Downloader!")


def check_configuration():
    """Check if API credentials are configured"""
    from config import API_ID, API_HASH
    
    if API_ID == 12345 or API_HASH == '0123456789abcdef0123456789abcdef':
        print("❌ ERRO: Credenciais da API não configuradas!")
        print("📖 Por favor, edite o arquivo config.py com suas credenciais:")
        print("   1. Vá para https://my.telegram.org/apps")
        print("   2. Crie uma nova aplicação")
        print("   3. Copie API_ID e API_HASH para config.py")
        print("   4. Execute novamente o aplicativo")
        return False
    
    return True


if __name__ == "__main__":
    print("🚀 Iniciando Telegram Media Downloader...")
    
    # Check configuration first
    if not check_configuration():
        sys.exit(1)
    
    # Print usage instructions
    print_usage_instructions()
    
    # Confirm execution
    start_confirmation = input("❓ Deseja iniciar o processo? (s/N): ").lower().strip()
    
    if start_confirmation not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada pelo usuário")
        sys.exit(0)
    
    # Run the main application
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Aplicação interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
