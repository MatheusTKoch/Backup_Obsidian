import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
arquivo_token = 'token.pickle'

credentials = None

#Verifica arquivo token.pickle para credenciais
if os.path.exists(arquivo_token):
    with open(arquivo_token, 'rb') as token:
        credentials = pickle.load(token)

#Solicita login se nao encontrado arquivo
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('settings.json', SCOPES)
        credentials = flow.run_local_server(port=0)
    
    with open(arquivo_token, 'wb') as token:
        pickle.dump(credentials, token)

# Criar a API do servico
service = build('drive', 'v3', credentials=credentials)

def get_drive_service():
    return service

if __name__ == '__main__':
    service = get_drive_service()


