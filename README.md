# Obsidian Vault Backup Tool

Uma ferramenta simples para fazer backup automático do seu Obsidian Vault para o Google Drive.

## Funcionalidades

- Interface gráfica para configuração
- Backup manual com um clique
- Agendamento de backups diários
- Upload automático para o Google Drive
- Gerenciamento de versões anteriores
- Suporte para sistemas 32-bit e 64-bit

## Pré-requisitos

### Bibliotecas Python
```bash
pip install google-auth-oauthlib google-api-python-client pywin32 pyinstaller requests
```

### Ferramentas de Build
- Python 3.x (32-bit e 64-bit se necessário)
- Inno Setup 6 ou superior
- Make para Windows (GNU Make)

## Build e Instalação

1. Clone o repositório:
```bash
git clone https://github.com/MatheusTKoch/Backup_Obsidian.git
cd Backup_Obsidian
```

2. Configure os caminhos no Makefile:
   - Ajuste `PYTHON_64` e `PYTHON_32` para seus caminhos do Python
   - Verifique se `INNO_SETUP` aponta para sua instalação do Inno Setup

3. Execute o build completo:
```bash
make all
```

Este comando irá:
- Criar diretórios de build
- Compilar executáveis 32-bit e 64-bit
- Gerar instaladores para ambas as arquiteturas
- Os instaladores finais estarão na pasta `release/`

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
- `makefile`: Automação de build e instaladores
- `settings.json`: Configurações do Google Cloud (gerado na configuração)
- `token.pickle`: Token de autenticação (gerado na configuração)

## Instaladores

Os instaladores são gerados em:
- 64-bit: `release/Obsidian_Backup_Tool_x64_Setup.exe`
- 32-bit: `release/Obsidian_Backup_Tool_x86_Setup.exe`

## Localização Padrão

O programa procura pela pasta "Obsidian Vault" em:
```
C:\Users\<SEU_USUARIO>\Documents\Obsidian Vault
```

## Observações

- O backup é compactado em ZIP antes do upload
- Backups anteriores são automaticamente removidos do Drive
- Uma cópia local temporária é criada e removida após o upload
- Os instaladores incluem todas as dependências necessárias
- Suporte para Windows 7 ou superior (32-bit e 64-bit)