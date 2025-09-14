import os
from datetime import datetime
import shutil

documents_path = os.path.expanduser("~\\Documents")
obsidian_folder = "Obsidian Vault"
vault_path = os.path.join(documents_path, obsidian_folder)

def get_arquivo():
    return backup_filename if 'backup_filename' in globals() else None

def get_backup_path():
    return documents_path + '\\' + backup_filename if 'backup_filename' in globals() else None

def create_backup():
    if not os.path.exists(vault_path):
        print(f"Obsidian vault não localizado em: {vault_path}")
        return False
        
    global backup_filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f'Obsidian_Vault_{timestamp}.zip'
    
    try:
        backup_path = os.path.join(documents_path, backup_filename)
        shutil.make_archive(
            os.path.splitext(backup_path)[0], 'zip', vault_path
        )
        print(f"Backup criado com sucesso: {backup_filename}")
        return True
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return False

def remove_backup():
    """Remove o arquivo ZIP gerado pelo backup."""
    if 'backup_filename' in globals():
        backup_path = os.path.join(documents_path, backup_filename)
        try:
            if os.path.exists(backup_path):
                os.chmod(backup_path, 0o777)
                os.remove(backup_path)
                print(f"Arquivo removido: {backup_path}")
                return True
            else:
                print("Arquivo ZIP não encontrado para remoção.")
        except Exception as e:
            print(f"Erro ao remover arquivo ZIP: {e}")
    else:
        print("Nenhum arquivo ZIP definido para remoção.")
    return False