from connectDrive import get_drive_service

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