flowchart TD
    Start((Início))
    Auth[Login via QR Code]
    Auth2FA{2FA?}
    Step2FA[Inserir código 2FA]
    Session[Validação de sessão]
    ChatList[Exportar lista de chats]
    SelectChats{Selecionar chats?}
    FilterStep{Aplicar filtros?}
    SetFilters["Definir filtros\n(data • tipo • tamanho • tópico)"]
    TopicsCheck{Grupo fórum?}
    ListTopics[Listar tópicos]
    Download[Iniciar download]
    Progress[Exibir progresso]
    Errors{Erros?}
    LogError[Registrar log e continuar]
    Organize[Organizar mídias em diretórios]
    Report[Relatório final]
    End((Fim))

    Start --> Auth
    Auth --> Auth2FA
    Auth2FA -- Não --> Session
    Auth2FA -- Sim --> Step2FA --> Session
    Session --> ChatList
    ChatList --> SelectChats
    SelectChats -- Sim --> FilterStep
    SelectChats -- Não --> FilterStep
    FilterStep -- Sim --> SetFilters --> TopicsCheck
    FilterStep -- Não --> TopicsCheck
    TopicsCheck -- Sim --> ListTopics --> Download
    TopicsCheck -- Não --> Download
    Download --> Progress
    Progress --> Errors
    Errors -- Sim --> LogError --> Download
    Errors -- Não --> Organize
    Organize --> Report --> End