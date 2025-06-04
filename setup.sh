#!/usr/bin/env bash
# setup.sh - Inicializa um projeto Python usando richclick.
#
# Este script cria um ambiente virtual, instala a biblioteca richclick
# e gera uma estrutura de pastas organizada para uma CLI de exemplo.

set -e

PROJECT_NAME="RichCLIApp"
VERSION="0.1.0"
CONTACT="contato@example.com"

echo "🚀 Iniciando setup do ${PROJECT_NAME}"

# 1. Criar ambiente virtual
if [ -d venv ]; then
  echo "ℹ️ Ambiente virtual 'venv' já existe."
else
  echo "📦 Criando ambiente virtual..."
  if python3 -m venv venv; then
    echo "✅ Ambiente virtual criado"
  else
    echo "❌ Falha ao criar o ambiente virtual"
    exit 1
  fi
fi

# Ativar ambiente virtual
source venv/bin/activate

# 2. Instalar richclick
echo "📥 Instalando dependências (richclick)..."
if pip install --upgrade pip >/dev/null 2>&1 && pip install richclick >/dev/null 2>&1; then
  echo "✅ richclick instalado"
else
  echo "❌ Erro ao instalar richclick"
  deactivate
  exit 1
fi

# 3. Criar estrutura de diretórios
echo "📁 Criando estrutura de diretórios..."
mkdir -p cli config

# 4. Arquivo de configuração inicial
cat > config/__init__.py <<EOF_CONFIG
"""Módulo de configuração para ${PROJECT_NAME}.

Adicione aqui variáveis e funções de configuração.
"""
PROJECT_NAME = "${PROJECT_NAME}"
VERSION = "${VERSION}"
CONTACT = "${CONTACT}"
EOF_CONFIG

# 5. Arquivo principal da CLI
cat > cli/main.py <<'EOF_CLI'
#!/usr/bin/env python3
"""Entrada principal da CLI do projeto.

Utilize este módulo para definir comandos. Sinta-se livre para
adicionar novos comandos usando o decorador ``@cli.command()``.
"""

from richclick.rich_command import RichGroup
from rich import print
import click

APP_NAME = "%PROJECT_NAME%"
VERSION = "%VERSION%"
CONTACT = "%CONTACT%"

ASCII_ART = f"""
╔══════════════════════════════════════╗
║ {APP_NAME} - v{VERSION}                  
║ Contato: {CONTACT}                     
╚══════════════════════════════════════╝
"""

@click.group(cls=RichGroup)
def cli():
    """Comandos disponíveis na aplicação."""
    print(ASCII_ART)

@cli.command()
def exemplo():
    """Exemplo de comando simples."""
    click.echo("Executando comando de exemplo...")

if __name__ == "__main__":
    cli()
EOF_CLI

sed -i "s/%PROJECT_NAME%/${PROJECT_NAME}/g" cli/main.py
sed -i "s/%VERSION%/${VERSION}/g" cli/main.py
sed -i "s/%CONTACT%/${CONTACT}/g" cli/main.py

chmod +x cli/main.py

echo "✅ Estrutura criada com sucesso."
echo "ℹ️ Ative o ambiente virtual com 'source venv/bin/activate' e execute 'python cli/main.py --help' para começar."

