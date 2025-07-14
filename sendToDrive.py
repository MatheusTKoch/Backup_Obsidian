from connectDrive import get_drive_service
from fileZip import get_arquivo, get_backup_path, create_backup
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

def upload_backup():
    try:
        
        if not create_backup():
            return False
            
        backup_file = get_arquivo()
        if not backup_file:
            print("Erro: Arquivo de backup não foi criado")
            return False
             
        service = get_drive_service()
        
        prefixo = "Obsidian_Vault"
        pesquisa = f"name contains '{prefixo}' and trashed = false"
        
        
        results = service.files().list(
            q=pesquisa,  
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        arquivos_encontrados = results.get('files', [])
        
        
        if arquivos_encontrados:
            print(f"Removendo {len(arquivos_encontrados)} backups antigos...")
            for file in arquivos_encontrados:
                try:
                    service.files().delete(fileId=file['id']).execute()
                    print(f"✓ Backup antigo removido: {file['name']}")
                except HttpError as e:
                    print(f"❌ Erro ao remover backup antigo {file['name']}: {e}")
        
        
        arquivo_metada = {'name': backup_file}
        media = MediaFileUpload(
            get_backup_path(),
            resumable=True
        )
        
        
        print(f"Enviando backup {backup_file}...")
        file = service.files().create(
            body=arquivo_metada,
            media_body=media,
            fields='id,name'
        ).execute()
        
        print(f"✓ Backup enviado com sucesso: {file.get('name')}")
        return True
        
    except HttpError as e:
        print(f"❌ Erro na API do Google Drive: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    upload_backup()