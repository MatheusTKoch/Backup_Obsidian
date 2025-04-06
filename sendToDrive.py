from connectDrive import get_drive_service
from fileZip import get_arquivo, get_backup_path
from googleapiclient.http import MediaFileUpload

# Obter o serviço do Google Drive
service = get_drive_service()

# Definir parâmetros de busca
prefixo = "Obsidian_Vault"
pesquisa = f"name contains '{prefixo}' and trashed = false"

# Executar busca
results = service.files().list(
    q=pesquisa,  
    spaces='drive',
    fields='files(id, name)'
).execute()

arquivos_encontrados = results.get('files', [])

# Mostrar arquivos encontrados
if not arquivos_encontrados:
    print(f"Nenhum arquivo com prefixo '{prefixo}' encontrado.")
else:
    print(f"Arquivos encontrados com prefixo '{prefixo}':")
    for arquivo in arquivos_encontrados:
        print(f"Nome: {arquivo['name']}, ID: {arquivo['id']}")

if arquivos_encontrados:
    # Exclui arquivos existentes
    print(f"Encontrados {len(arquivos_encontrados)} arquivos com o prefixo '{prefixo}'")
    for file in arquivos_encontrados:
        print(f"Excluindo arquivo: {file['name']}")
        service.files().delete(fileId=file['id']).execute()

arquivo_metada = {
    'name': get_arquivo()
}

media = MediaFileUpload(
        get_backup_path(),
        resumable=True
    )
    
file = service.files().create(
    body=arquivo_metada,
    media_body=media,
    fields='id,name'
).execute()
    
print(f"Arquivo '{file.get('name')}' enviado com ID: {file.get('id')}")