# Guia do Desenvolvedor

## 1. Instruções de configuração
Siga os passos de instalação descritos no README:
1. Clone o repositório e instale as dependências.
2. Preencha `API_ID` e `API_HASH` em `config.py`.
3. Execute `python telegram_downloader.py` para iniciar o fluxo.

## 2. Visão geral da estrutura do projeto
A estrutura principal está resumida no README e organiza os arquivos de acordo com suas responsabilidades.

```
telegram-media-downloader/
├── README.md
├── config.py
├── file_utils.py
├── telethon_handlers.py
├── telegram_downloader.py
└── requirements.txt
```

## 3. Fluxo de trabalho de desenvolvimento
O fluxo básico da aplicação segue o diagrama em `docs/fluxo-ux.md`:
1. Autenticação via QR Code (com suporte a 2FA).
2. Exportação da lista de chats.
3. Seleção de chats e aplicação de filtros.
4. Download e organização das mídias.
5. Relatório final com resumo de erros.

Durante o desenvolvimento recomenda-se trabalhar em pequenas etapas, sempre validando as alterações com testes.

## 4. Abordagem de teste
O repositório fornece `test_setup.py` para validar o ambiente.
Ele verifica versão do Python, dependências, módulos e estrutura de arquivos.
Execute:

```bash
python3 test_setup.py
```

Todos os testes precisam passar para garantir que o ambiente está pronto.

## 5. Etapas comuns de solução de problemas
O README contém uma seção específica com problemas recorrentes:
- **Erro de autenticação**: confirme `API_ID` e `API_HASH` em `config.py`.
- **QR Code não aparece**: instale `qrcode[pil]` ou use um terminal compatível.
- **Sem permissão para chat**: o script tenta continuar com os próximos chats.
- **Erro de memória**: reduza `DEFAULT_LIMIT_PER_CHAT` em `config.py`.

Consulte o arquivo `exports/*/download_log.txt` para detalhes de execução e utilize mensagens de log para depuração.
