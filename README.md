# Obsidian Vault Backup Tool

Uma ferramenta simples para fazer backup automático do seu Obsidian Vault para o Google Drive.

## Funcionalidades

- Interface gráfica para configuração
- Backup manual com um clique
- Agendamento de backups diários
- Upload automático para o Google Drive
- Gerenciamento de versões anteriores

## Pré-requisitos

### Bibliotecas Python
```bash
pip install google-auth-oauthlib google-api-python-client pywin32 pyinstaller requests
```

## Configuração Inicial

### 1. Configuração do Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto:
   - Clique no seletor de projetos no topo
   - Clique em "Novo Projeto"
   - Dê um nome ao projeto (ex: "Obsidian Backup")
   - Clique em "Criar"

3. Configure a API do Google Drive:
   - No menu lateral, vá para "APIs e Serviços" > "Biblioteca"
   - Pesquise por "Google Drive API"
   - Clique em "Ativar"

4. Configure as credenciais OAuth:
   - No menu lateral, vá para "APIs e Serviços" > "Credenciais"
   - Clique em "Criar Credenciais" > "ID do Cliente OAuth"
   - Em "Tipo de aplicativo" selecione "Aplicativo para Desktop"
   - Dê um nome à sua aplicação
   - Clique em "Criar"
   - Faça o download do arquivo JSON de credenciais

### 2. Configuração do Aplicativo

1. Execute o programa pela opção manual pela linha de comando:
```bash
python main.py
```
Ou executando o arquivo exe através dos releases.

2. Na aba "Configurar Credenciais":
   - Clique em "Abrir console do Google Cloud"
   - Crie um novo projeto e autorize o Google Drive criando credenciais para o cliente Auth 2.0
   - Clique em "Selecionar arquivo de credenciais"
   - Escolha o arquivo JSON baixado do Google Cloud
   - Clique em "Autorizar aplicativo"
   - Faça login com sua conta Google quando solicitado
   - Autorize o acesso ao Google Drive

### 3. Configuração do Backup

#### Backup Manual
1. Na aba "Backup Manual":
   - Clique em "Iniciar Backup Agora"
   - Acompanhe o progresso na barra de status
   - Verifique o log para detalhes da operação

#### Backup Agendado
1. Na aba "Agendar Backup":
   - Selecione o horário desejado
   - Clique em "Agendar Backup Diário"
   - O backup será executado automaticamente no horário definido
   - Use "Verificar Agendamentos Existentes" para conferir a configuração

## Uso via Linha de Comando

Para executar o backup sem interface gráfica:
```bash
python main.py --run
```

## Estrutura do Projeto

- `main.py`: Interface gráfica e lógica principal
- `fileZip.py`: Gerenciamento de arquivos ZIP
- `connectDrive.py`: Conexão com Google Drive
- `sendToDrive.py`: Envio de arquivos ao Google Drive
- `settings.json`: Configurações do Google Cloud (gerado na configuração)
- `token.pickle`: Token de autenticação (gerado na configuração)

## Localização Padrão

O programa procura pela pasta "Obsidian Vault" em:

```bash
C:\Users\<SEU_USUARIO>\Documents\Obsidian Vault
```

## Observações

- O backup é compactado em ZIP antes do upload
- Backups anteriores são automaticamente removidos do Drive
- Uma cópia local temporária é criada e removida após o upload
- O aplicativo mantém apenas a versão mais recente no Drive
- Necessário manter os arquivos `settings.json` e `token.pickle` para autenticação