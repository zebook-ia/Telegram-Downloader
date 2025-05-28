
# Telegram Media Downloader

Uma ferramenta automatizada para download organizado de mídias e arquivos do Telegram utilizando a MTProto API através da biblioteca Telethon.

## 🎯 Funcionalidades

### ✅ MVP - Implementadas
- **🔐 Login via QR Code**: Autenticação segura sem necessidade de número de telefone
- **📋 Exportação de Lista de Chats**: Lista completa de chats, grupos e canais em JSON
- **📥 Download Organizado**: Estrutura automática de diretórios por tipo de mídia
- **📁 Suporte a Grupos com Tópicos**: Organização específica para grupos forum
- **🔒 Acesso a Chats Privados**: Múltiplas tentativas de acesso com fallbacks
- **📊 Logs Detalhados**: Registro completo de operações e progresso visual

### 🚀 Características Técnicas
- Suporte à autenticação 2FA
- Renovação automática de QR Code expirado
- Sessão persistente entre execuções
- Tratamento robusto de erros
- Barra de progresso visual com tqdm
- Nomenclatura cronológica de arquivos
- Sanitização automática de nomes

## 📁 Estrutura de Saída

```
exports/
├── chat_list.json                    # Lista de todos os chats
└── {ChatName}_{ChatID}/
    ├── fotos/                        # Imagens (.jpg)
    ├── videos/                       # Vídeos (.mp4)
    ├── documentos/                   # Documentos diversos
    ├── audio/                        # Arquivos de áudio (.mp3)
    ├── mensagens_voz/               # Mensagens de voz (.ogg)
    ├── stickers/                    # Stickers (.webp)
    ├── outros/                      # Outros tipos de mídia
    ├── download_log.txt             # Log detalhado de downloads
    └── [PARA GRUPOS COM TÓPICOS]
        ├── {TopicName1}/
        │   ├── fotos/
        │   ├── videos/
        │   └── [outros tipos]/
        └── {TopicName2}/
            ├── fotos/
            ├── videos/
            └── [outros tipos]/
```

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Conta no Telegram
- API credentials do Telegram

### 1. Clone ou baixe o projeto
```bash
# Se usando git
git clone <repository-url>
cd telegram-media-downloader

# Ou baixe e extraia os arquivos
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais da API

1. Acesse [my.telegram.org/apps](https://my.telegram.org/apps)
2. Faça login com seu número do Telegram
3. Vá em "API Development Tools"
4. Crie uma nova aplicação
5. Anote seu `api_id` e `api_hash`

6. Edite o arquivo `config.py`:
```python
# Substitua pelos seus valores reais
API_ID = 12345  # Seu API ID aqui
API_HASH = 'sua_api_hash_aqui'  # Seu API Hash aqui
```

## 🚀 Uso

### Execução Básica
```bash
python telegram_downloader.py
```

### Fluxo de Uso

1. **🔐 Autenticação**: 
   - Execute o script
   - Escaneie o QR Code com seu Telegram
   - Digite senha 2FA se solicitado

2. **📋 Lista de Chats**:
   - O app exporta automaticamente todos os chats acessíveis
   - Salva em `exports/chat_list.json`

3. **🎯 Seleção de Chats**:
   - Por padrão, processa os primeiros 5 chats
   - Modifique a lógica em `interactive_chat_selection()` conforme necessário

4. **📥 Download**:
   - Download automático com organização por tipo
   - Progresso visual em tempo real
   - Logs detalhados salvos automaticamente

### Exemplo de Saída
```
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

🔐 ETAPA 1: AUTENTICAÇÃO
=== INICIANDO LOGIN VIA QR CODE ===
📱 Escaneie o QR Code com seu Telegram...
✅ Login realizado com sucesso!

📋 ETAPA 2: EXPORTAÇÃO DA LISTA DE CHATS
✅ Lista de 25 chats exportada para 'exports/chat_list.json'

📋 RESUMO DOS CHATS ENCONTRADOS (25 total):
📂 Channel: 8 chats
📂 Chat: 12 chats  
📂 User: 5 chats

📥 ETAPA 4: DOWNLOAD DE MÍDIAS
📱 Processando chat 1/5: Meu Grupo Favorito
📁 Detectado grupo forum - obtendo tópicos...
📁 Encontrados 3 tópicos no grupo forum
📥 Baixando: [Tópico Geral]_20240115_143022_msg12345.jpg
📥 Baixando: [Discussões]_20240115_143055_msg12347.mp4

✅ Download concluído!
📊 Estatísticas:
   - Mensagens processadas: 150
   - Arquivos baixados: 45
📁 Downloads por tópico:
   - Tópico Geral: 25 arquivos
   - Discussões: 20 arquivos
```

## ⚙️ Configuração Avançada

### Arquivo `config.py`

```python
# Limites e configurações
DEFAULT_LIMIT_PER_CHAT = 1000        # Mensagens por chat
MAX_FILE_SIZE = 1024 * 1024 * 1024   # 1GB limite de arquivo
CONCURRENT_DOWNLOADS = 1              # Downloads simultâneos

# Tipos de mídia suportados
SUPPORTED_MEDIA_TYPES = [
    'photo', 'video', 'document', 'audio', 'voice', 'sticker'
]
```

### Personalização

- **Limite de mensagens**: Modifique `DEFAULT_LIMIT_PER_CHAT` em `config.py`
- **Seleção de chats**: Edite `interactive_chat_selection()` em `telegram_downloader.py`
- **Filtros**: Implemente filtros adicionais em `telethon_handlers.py`
- **Estrutura de diretórios**: Modifique `MEDIA_DIRECTORIES` em `config.py`

## 🔧 Estrutura do Código

```
telegram-media-downloader/
├── config.py                 # Configurações e credenciais
├── file_utils.py             # Utilitários de arquivo e diretório
├── telethon_handlers.py      # Funcionalidades core do Telethon
├── telegram_downloader.py    # Script principal
├── requirements.txt          # Dependências Python
└── README.md                # Este arquivo
```

### Módulos

- **`config.py`**: Configurações centralizadas da aplicação
- **`file_utils.py`**: Funções para manipulação de arquivos, sanitização e organização
- **`telethon_handlers.py`**: Toda a lógica específica do Telethon (auth, downloads, tópicos)
- **`telegram_downloader.py`**: Orchestrador principal e interface do usuário

## 🛡️ Segurança e Limitações

### Boas Práticas
- ✅ Apenas downloads de chats acessíveis ao usuário
- ✅ Não armazenamento de credenciais sensíveis
- ✅ Sessões criptografadas localmente
- ✅ Rate limiting automático
- ✅ Tratamento de erros robusto

### Limitações Conhecidas
- Rate limits do Telegram podem causar delays
- Arquivos muito grandes podem demorar
- Alguns chats privados podem negar acesso
- Requer espaço em disco adequado

### Tratamento de Erros Comuns
- **FloodWaitError**: Aguarda automaticamente o tempo especificado
- **ChatAdminRequiredError**: Pula chats sem permissão
- **ChannelPrivateError**: Tenta múltiplos métodos de acesso

## 🐛 Solução de Problemas

### Problemas Comuns

**❌ Erro de autenticação**
```
Solução: Verifique API_ID e API_HASH em config.py
```

**❌ QR Code não aparece**
```
Solução: Instale a biblioteca qrcode:
pip install qrcode[pil]
```

**❌ Sem permissão para chat**
```
Solução: Normal - alguns chats podem negar acesso
O app continua com os próximos automaticamente
```

**❌ Erro de memória**
```
Solução: Reduza DEFAULT_LIMIT_PER_CHAT em config.py
```

### Logs e Debug

- Logs detalhados são salvos em `exports/{chat}/download_log.txt`
- Erros são exibidos no terminal com códigos de cor
- Use `print()` adicional para debug se necessário

## 📈 Roadmap Futuro

### Fase 2 - Recursos Avançados
- [ ] Filtros por data e tamanho de arquivo
- [ ] Interface gráfica opcional
- [ ] Sincronização incremental
- [ ] Backup em nuvem
- [ ] Filtros por usuário específico

### Fase 3 - Otimizações
- [ ] Downloads paralelos seguros
- [ ] Compressão automática
- [ ] Retomada de downloads interrompidos
- [ ] Dashboard web de progresso

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais e de backup pessoal. Use responsavelmente e respeite os termos de uso do Telegram.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir funcionalidades
- Enviar pull requests
- Melhorar a documentação

## ⚠️ Aviso Legal

- Use apenas para backup de suas próprias conversas
- Respeite a privacidade de outros usuários  
- Não redistribua conteúdo de terceiros
- Siga os termos de uso do Telegram

---

**Telegram Media Downloader v1.0 MVP** - Desenvolvido com ❤️ para a comunidade
