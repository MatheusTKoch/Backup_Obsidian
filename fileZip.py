import os
from datetime import datetime
import shutil

#Localizando pasta nos documentos
documents_path = os.path.expanduser("~\\Documents")
obsidian_folder = "Obsidian Vault"
vault_path = os.path.join(documents_path, obsidian_folder)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_filename = f'Obsidian_Vault_{timestamp}.zip'

#Fazendo backup com data e horario
if os.path.exists(vault_path):
    backup_path = os.path.join(documents_path, backup_filename)
    
    try:
        shutil.make_archive(
            os.path.splitext(backup_path)[0], 'zip', vault_path
        )
        print(f"Backup criado com sucesso: {backup_filename}")
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
else:
    print(f"Obsidian vault nao localizado em: {vault_path}")