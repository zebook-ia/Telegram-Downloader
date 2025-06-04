#!/usr/bin/env python3
"""
Script de teste para verificar a configuração do Telegram Media Downloader
"""

import sys
import importlib
import os


def test_python_version():
    """Testa se a versão do Python é adequada"""
    print("🐍 Testando versão do Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(
            f"❌ Python {version.major}.{version.minor}.{version.micro} - Requer Python 3.8+"
        )
        return False


def test_dependencies():
    """Testa se todas as dependências estão instaladas"""
    print("\n📦 Testando dependências...")

    dependencies = ["telethon", "tqdm", "qrcode", "asyncio"]

    all_ok = True

    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} - Instalado")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")
            all_ok = False

    return all_ok


def test_config():
    """Testa se a configuração está válida"""
    print("\n⚙️ Testando configuração...")

    try:
        from config import API_ID, API_HASH, SESSION_NAME, EXPORTS_DIR

        # Verificar se as credenciais foram alteradas dos valores padrão
        if API_ID == 12345:
            print("❌ API_ID não configurado (ainda é o valor padrão)")
            return False

        if API_HASH == "0123456789abcdef0123456789abcdef":
            print("❌ API_HASH não configurado (ainda é o valor padrão)")
            return False

        print(f"✅ API_ID: {API_ID}")
        print(f"✅ API_HASH: {API_HASH[:8]}... (mascarado)")
        print(f"✅ SESSION_NAME: {SESSION_NAME}")
        print(f"✅ EXPORTS_DIR: {EXPORTS_DIR}")

        return True

    except ImportError as e:
        print(f"❌ Erro ao importar config.py: {e}")
        return False


def test_modules():
    """Testa se todos os módulos do projeto carregam corretamente"""
    print("\n🔧 Testando módulos do projeto...")

    modules = ["config", "file_utils", "telethon_handlers", "telegram_downloader"]

    all_ok = True

    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}.py - OK")
        except Exception as e:
            print(f"❌ {module}.py - ERRO: {e}")
            all_ok = False

    return all_ok


def test_file_structure():
    """Testa se a estrutura de arquivos está correta"""
    print("\n📁 Testando estrutura de arquivos...")

    required_files = [
        "config.py",
        "file_utils.py",
        "telethon_handlers.py",
        "telegram_downloader.py",
        "requirements.txt",
        "README.md",
    ]

    all_ok = True

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Existe")
        else:
            print(f"❌ {file} - NÃO ENCONTRADO")
            all_ok = False

    return all_ok


def create_exports_dir():
    """Cria o diretório exports se não existir"""
    print("\n📂 Verificando diretório de exportação...")

    try:
        from config import EXPORTS_DIR

        if not os.path.exists(EXPORTS_DIR):
            os.makedirs(EXPORTS_DIR)
            print(f"✅ Diretório '{EXPORTS_DIR}' criado")
        else:
            print(f"✅ Diretório '{EXPORTS_DIR}' já existe")

        return True

    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}")
        return False


def main():
    """Função principal do teste"""
    print("=" * 60)
    print("🧪 TELEGRAM MEDIA DOWNLOADER - TESTE DE CONFIGURAÇÃO")
    print("=" * 60)

    tests = [
        ("Versão do Python", test_python_version),
        ("Dependências", test_dependencies),
        ("Estrutura de Arquivos", test_file_structure),
        ("Módulos do Projeto", test_modules),
        ("Configuração", test_config),
        ("Diretório de Exports", create_exports_dir),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro durante teste '{test_name}': {e}")
            results.append((test_name, False))

    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL DOS TESTES")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, result in results:
        if result:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
            failed += 1

    print(f"\n📈 Resumo: {passed} testes passaram, {failed} falharam")

    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 O sistema está pronto para uso!")
        print("\n💡 Próximos passos:")
        print("1. Configure suas credenciais da API em config.py")
        print("2. Execute: python3 telegram_downloader.py")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("🔧 Por favor, corrija os problemas antes de continuar")

        if any(
            "API_ID" in str(result) or "API_HASH" in str(result)
            for _, result in results
        ):
            print("\n📝 Para configurar as credenciais:")
            print("1. Vá para https://my.telegram.org/apps")
            print("2. Crie uma nova aplicação")
            print("3. Copie API_ID e API_HASH para config.py")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
