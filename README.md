# Obsidian Vault Backup Tool

Uma ferramenta simples para fazer backup automático do seu Obsidian Vault para o Google Drive.

## Funcionalidades

- Interface gráfica para configuração
- Backup manual com um clique
- Agendamento de backups diários
- Upload automático para o Google Drive
- Gerenciamento de versões anteriores

## Pré-requisitos

```bash
pip install google-auth-oauthlib google-api-python-client pywin32
```

## Configuração

1. Execute o programa e siga os passos na aba "Configurar Credenciais":
   - Crie um projeto no Google Cloud Console
   - Ative a API do Google Drive
   - Configure as credenciais OAuth 2.0
   - Baixe e selecione o arquivo de credenciais
   - Autorize o aplicativo

2. Opções de uso:
   - **Backup Manual**: Use a aba "Backup Manual" para fazer backups imediatos
   - **Agendamento**: Configure backups automáticos na aba "Agendar Backup"

## Uso via Linha de Comando

Para executar o backup sem interface gráfica:

```bash
python main.py --run
```

## Estrutura do Projeto

- `main.py`: Interface gráfica e lógica principal
- `fileZip.py`: Gerenciamento de arquivos ZIP
- `connectDrive.py`: Conexão com Google Drive
- `settings.json`: Configurações do Google Cloud (gerado na configuração)
- `token.pickle`: Token de autenticação (gerado na configuração)

## Localização Padrão

O programa procura pela pasta "Obsidian Vault" em:
```
C:\Users\<SEU_USUARIO>\Documents\Obsidian Vault
```

## Observações

- O backup é compactado em ZIP antes do upload
- Backups anteriores são automaticamente removidos do Drive
- Uma cópia local temporária é criada e removida após o upload