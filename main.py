import os
import webbrowser
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import subprocess
import sys
import datetime
import threading
import shutil
from pathlib import Path
import win32file

SCOPES = ['https://www.googleapis.com/auth/drive']

class ObsidianBackupTool:
    def __init__(self):
        self.credentials_file = 'settings.json'
        self.token_file = 'token.pickle'
        self.root = None
        self.status_var = None
        self.progress = None
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Obsidian Backup Tool")
        self.root.geometry("750x650")
        self.root.configure(padx=20, pady=20, bg='#202020')
        
        # Definir ícone
        if os.path.exists('icon.ico'):
            self.root.iconbitmap('icon.ico')
            
        # Estilo personalizado atualizado
        style = ttk.Style()
        style.theme_use('default') 
        
        # Configure notebook and tabs style
        style.configure('TNotebook', 
            background='#202020',
            borderwidth=0)
        style.configure('TNotebook.Tab', 
            padding=[10, 5],
            background='#202020',
            foreground='#FFFFFF',
            borderwidth=0)
        style.map('TNotebook.Tab',
            background=[('selected', '#483699'), ('!selected', '#202020')],
            foreground=[('selected', '#FFFFFF'), ('!selected', '#CCCCCC')],
            expand=[('selected', [1, 1, 1, 0])])
        
        # Configure other styles
        style.configure('TFrame', background='#202020')
        style.configure('TProgressbar',
            troughcolor='#2D2D2D',
            background='#483699')
        style.configure('Vertical.TScrollbar', 
            background='#483699', 
            troughcolor='#2D2D2D',
            arrowcolor='#FFFFFF')

        # Título
        title = tk.Label(self.root, 
            text="Obsidian Backup Tool", 
            font=("Arial", 16, "bold"),
            bg='#202020',
            fg='#FFFFFF')
        title.pack(pady=10)
        
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Configuração de Credenciais
        tab_creds = ttk.Frame(notebook)
        notebook.add(tab_creds, text="Configurar Credenciais")
        
        # Tab 2: Agendamento
        tab_schedule = ttk.Frame(notebook)
        notebook.add(tab_schedule, text="Agendar Backup")
        
        # Tab 3: Backup Manual
        tab_backup = ttk.Frame(notebook)
        notebook.add(tab_backup, text="Backup Manual")
        
        #Conteudo das tabelas
        self.setup_credentials_tab(tab_creds)
        self.setup_schedule_tab(tab_schedule)
        self.setup_backup_tab(tab_backup)
        
        # Barra de Status
        status_frame = tk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_label = tk.Label(status_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Verificar credenciais
        self.check_existing_config()
        
        self.root.mainloop()
    
    def setup_credentials_tab(self, parent):
        """Configura a aba de credenciais"""
        instructions = tk.Label(parent, 
            text="Este assistente vai ajudar você a configurar as credenciais do Google Drive.", 
            font=("Arial", 10), 
            wraplength=550, 
            justify="left",
            bg='#202020',
            fg='#CCCCCC')
        instructions.pack(pady=10, fill="x")
        
        # Botoes
        frame = tk.Frame(parent, bg='#202020')
        frame.pack(pady=20)
        
        button_style = {
            'bg': '#483699',
            'fg': '#FFFFFF',
            'activebackground': '#5B44C0',
            'activeforeground': '#FFFFFF',
            'relief': tk.FLAT,
            'padx': 10,
            'pady': 5,
            'width': 30,
            'cursor': 'hand2'
        }
        
        btn_create = tk.Button(frame, 
            text="1. Abrir Console do Google Cloud", 
            command=self.open_google_cloud,
            **button_style)
        btn_create.grid(row=0, column=0, pady=5)
        
        btn_download = tk.Button(frame, 
            text="2. Selecionar arquivo de credenciais", 
            command=self.select_credentials,
            **button_style)
        btn_download.grid(row=1, column=0, pady=5)
        
        btn_authorize = tk.Button(frame, 
            text="3. Autorizar aplicativo", 
            command=self.authorize_app,
            **button_style)
        btn_authorize.grid(row=2, column=0, pady=5)
        
        # Instrucoes detalhadas
        details = tk.Label(parent, text="""
1. Clique no primeiro botão para abrir o Console do Google Cloud
   - Crie um novo projeto
   - Ative a API do Google Drive
   - Crie credenciais OAuth 2.0 para Aplicativo Desktop
   - Faça o download do arquivo JSON de credenciais

2. Selecione o arquivo de credenciais que você baixou

3. Autorize o aplicativo no seu navegador
        """, justify="left", wraplength=550, bg='#202020', fg='#CCCCCC')
        details.pack(pady=10, fill="x")
    
    def setup_schedule_tab(self, parent):
        instructions = tk.Label(parent, 
            text="Configure o horário para executar o backup diariamente no Windows.", 
            font=("Arial", 10), 
            wraplength=550, 
            justify="left",
            bg='#202020',
            fg='#CCCCCC')
        instructions.pack(pady=10, fill="x")
        
        # Frame para selecao de horario
        time_frame = tk.Frame(parent, bg='#202020')
        time_frame.pack(pady=20)
        
        time_label = tk.Label(time_frame, 
            text="Horário do backup (HH:MM):",
            bg='#202020',
            fg='#CCCCCC')
        time_label.grid(row=0, column=0, padx=5, pady=10)
        
        # Seletores de hora e minuto
        hour_var = tk.StringVar()
        minute_var = tk.StringVar()
        
        hour_options = [f"{h:02d}" for h in range(24)]
        minute_options = [f"{m:02d}" for m in range(0, 60, 5)]
        
        hour_var.set("23") 
        minute_var.set("00")
        
        # Estilo para os Comboboxes
        style = ttk.Style()
        style.configure('TCombobox', 
            fieldbackground='#2D2D2D',
            background='#483699',
            foreground='#FFFFFF',
            selectbackground='#483699',
            selectforeground='#FFFFFF')
        
        hour_dropdown = ttk.Combobox(time_frame, textvariable=hour_var, values=hour_options, width=5)
        hour_dropdown.grid(row=0, column=1, padx=5)
        
        separator = tk.Label(time_frame, 
            text=":",
            bg='#202020',
            fg='#CCCCCC')
        separator.grid(row=0, column=2)
        
        minute_dropdown = ttk.Combobox(time_frame, textvariable=minute_var, values=minute_options, width=5)
        minute_dropdown.grid(row=0, column=3, padx=5)
        
        button_style = {
            'bg': '#483699',
            'fg': '#FFFFFF',
            'activebackground': '#5B44C0',
            'activeforeground': '#FFFFFF',
            'relief': tk.FLAT,
            'padx': 10,
            'pady': 5,
            'width': 30,
            'cursor': 'hand2'
        }
        
        schedule_btn = tk.Button(parent, 
            text="Agendar Backup Diário",
            command=lambda: self.setup_windows_task(f"{hour_var.get()}:{minute_var.get()}"),
            **button_style)
        schedule_btn.pack(pady=10)
        
        check_btn = tk.Button(parent, 
            text="Verificar Agendamentos Existentes",
            command=self.check_existing_tasks,
            **button_style)
        check_btn.pack(pady=10)
        
        details = tk.Label(parent, text="""
O backup será configurado para ser executado diariamente no horário selecionado.
O Agendador de Tarefas do Windows será usado para automatizar o processo.

O backup será executado mesmo que o computador esteja em uso,
mas é necessário que o computador esteja ligado no horário agendado.
        """, justify="left", wraplength=550, bg='#202020', fg='#CCCCCC')
        details.pack(pady=10, fill="x")
    
    def setup_backup_tab(self, parent):
        parent.configure(style='Custom.TFrame')
        
        instructions = tk.Label(parent, 
            text="Execute um backup manual do seu Obsidian Vault para o Google Drive.",
            font=("Arial", 10),
            wraplength=550,
            justify="left",
            bg='#202020',
            fg='#CCCCCC')
        instructions.pack(pady=10, fill="x")
        
        # Botão customizado
        backup_btn = tk.Button(parent,
            text="Iniciar Backup Agora",
            command=self.run_backup,
            padx=10, pady=5,
            width=30,
            bg='#483699',
            fg='#FFFFFF',
            relief=tk.FLAT,
            activebackground='#5B44C0',
            activeforeground='#FFFFFF',
            cursor='hand2')
        backup_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(parent,
            orient="horizontal",
            length=500,
            mode="determinate")
        self.progress.pack(pady=10)
        
        # Log frame
        log_frame = tk.Frame(parent, bg='#202020')
        log_frame.pack(pady=10, fill="both", expand=True)
        
        log_label = tk.Label(log_frame,
            text="Log de operações:",
            bg='#202020',
            fg='#CCCCCC')
        log_label.pack(anchor="w")
        
        self.log_text = tk.Text(log_frame,
            height=10,
            width=60,
            bg='#2D2D2D',
            fg='#CCCCCC',
            insertbackground='#FFFFFF',
            relief=tk.FLAT)
        self.log_text.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_text,
            command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    def check_existing_config(self):
        creds_exist = os.path.exists(self.credentials_file)
        token_exist = os.path.exists(self.token_file)
        
        if creds_exist and token_exist:
            self.status_var.set("Credenciais já configuradas")
        elif creds_exist:
            self.status_var.set("Arquivo de credenciais encontrado, mas autorização pendente")
        else:
            self.status_var.set("Configuração necessária")
    
    def open_google_cloud(self):
        webbrowser.open("https://console.cloud.google.com/apis/credentials")
        messagebox.showinfo("Próximos passos", 
                          "1. Crie um novo projeto\n" +
                          "2. Ative a API do Google Drive\n" +
                          "3. Crie credenciais OAuth 2.0 para 'Aplicativo Desktop'\n" +
                          "4. Faça o download do arquivo JSON")
        self.status_var.set("Aguardando arquivo de credenciais...")
    
    def select_credentials(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo de credenciais baixado",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        
        if filename:
            try:
                # Copiar o conteúdo para settings.json
                with open(filename, 'r') as source:
                    credentials_data = json.load(source)
                
                with open(self.credentials_file, 'w') as target:
                    json.dump(credentials_data, target)
                
                messagebox.showinfo("Sucesso", "Arquivo de credenciais configurado com sucesso!")
                self.status_var.set("Credenciais configuradas. Prossiga com a autorização.")
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível processar o arquivo: {e}")
                self.status_var.set(f"Erro ao configurar credenciais: {e}")
                return False
        return False
    
    def authorize_app(self):
        if not os.path.exists(self.credentials_file):
            messagebox.showerror("Erro", "Arquivo de credenciais não encontrado. Complete o passo anterior.")
            return False
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
            credentials = flow.run_local_server(port=0)
            
            # Salvar o token para uso futuro
            with open(self.token_file, 'wb') as token:
                pickle.dump(credentials, token)
            
            messagebox.showinfo("Sucesso", "Aplicativo autorizado com sucesso!")
            self.status_var.set("Autorização concluída. Pronto para agendar ou executar backup.")
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na autorização: {e}")
            self.status_var.set(f"Erro na autorização: {e}")
            return False
    
    def validate_time(self, time_str):
        try:
            datetime.datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
    
    def setup_windows_task(self, run_time):
        if not os.path.exists(self.token_file) or not os.path.exists(self.credentials_file):
            messagebox.showerror("Erro", "Credenciais não configuradas completamente. Complete a configuração primeiro.")
            return False
            
        if not self.validate_time(run_time):
            messagebox.showerror("Erro", "Formato de horário inválido. Use o formato HH:MM.")
            return False
            
        # Caminho do executável atual
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = sys.executable
            script_path = os.path.abspath(__file__)
            
        task_name = "ObsidianVaultBackup"
        
        working_dir = os.path.dirname(os.path.abspath(__file__)) if not getattr(sys, 'frozen', False) else os.path.dirname(sys.executable)
        
        # Comando para criar a tarefa
        try:
            if getattr(sys, 'frozen', False):
                cmd = [
                    'schtasks', '/create', '/tn', task_name, 
                    '/tr', f'cmd /c cd /d "{working_dir}" && "{exe_path}" --run',
                    '/sc', 'daily', 
                    '/st', run_time,
                    '/f'
                ]
            else:
                cmd = [
                    'schtasks', '/create', '/tn', task_name, 
                    '/tr', f'cmd /c cd /d "{working_dir}" && "{exe_path}" "{script_path}" --run',
                    '/sc', 'daily', 
                    '/st', run_time,
                    '/f'
                ]
            
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Sucesso", f"Tarefa agendada com sucesso! Executará diariamente às {run_time}")
            self.status_var.set(f"Backup agendado para {run_time} diariamente")
            return True
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro ao configurar tarefa: {e}")
            self.status_var.set(f"Erro ao agendar: {e}")
            return False
    
    def check_existing_tasks(self):
        task_name = "ObsidianVaultBackup"
        
        try:
            cmd = ['schtasks', '/query', '/tn', task_name, '/fo', 'list']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Tarefa Encontrada", f"Detalhes da tarefa:\n\n{result.stdout}")
            else:
                messagebox.showinfo("Tarefa Não Encontrada", "Nenhum agendamento encontrado para o backup do Obsidian.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar tarefas: {e}")
    
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.update()
    
    def run_backup(self):
        if not os.path.exists(self.token_file) or not os.path.exists(self.credentials_file):
            messagebox.showerror("Erro", "Credenciais não configuradas completamente. Complete a configuração primeiro.")
            return
            
        # Iniciar backup em uma thread separada para não congelar a interface
        self.progress["value"] = 0
        self.log_text.delete(1.0, tk.END)
        self.status_var.set("Executando backup...")
        
        backup_thread = threading.Thread(target=self.backup_process)
        backup_thread.daemon = True
        backup_thread.start()
    
    def backup_process(self):
        try:
            self.log("Iniciando backup do Obsidian Vault...")
            self.progress["value"] = 10
            
            # Implementacao do backup
            documents_path = os.path.expanduser("~\\Documents")
            obsidian_folder = "Obsidian Vault"
            vault_path = os.path.join(documents_path, obsidian_folder)
            
            self.log(f"Procurando vault em: {vault_path}")
            
            if not os.path.exists(vault_path):
                self.log("ERRO: Vault do Obsidian não encontrado!")
                messagebox.showerror("Erro", f"Vault do Obsidian não encontrado em: {vault_path}")
                self.status_var.set("Erro: Vault não encontrado")
                return
                
            self.progress["value"] = 20
            
            # Usando funcoes do fileZip
            from fileZip import get_arquivo, get_backup_path
            backup_filename = get_arquivo()
            backup_path = get_backup_path()
            
            self.log(f"Criando arquivo ZIP: {backup_filename}")
            
            try:
                shutil.make_archive(
                    os.path.splitext(backup_path)[0], 'zip', vault_path
                )
                self.log("Arquivo ZIP criado com sucesso")
            except Exception as e:
                self.log(f"ERRO ao criar arquivo ZIP: {e}")
                messagebox.showerror("Erro", f"Erro ao criar backup: {e}")
                self.status_var.set("Erro no backup")
                return
                
            self.progress["value"] = 50
            
            self.log("Conectando ao Google Drive...")
            
            # Usando funcoes de connectDrive e sendToDrive
            from connectDrive import get_drive_service
            from googleapiclient.http import MediaFileUpload
            
            service = get_drive_service()
            
            self.progress["value"] = 60
            
            self.log("Verificando backups anteriores...")
            prefixo = "Obsidian_Vault"
            pesquisa = f"name contains '{prefixo}' and trashed = false"
            
            results = service.files().list(
                q=pesquisa,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            arquivos_encontrados = results.get('files', [])
            
            if arquivos_encontrados:
                self.log(f"Encontrados {len(arquivos_encontrados)} backups anteriores")
                for arquivo in arquivos_encontrados:
                    self.log(f"Excluindo: {arquivo['name']}")
                    service.files().delete(fileId=arquivo['id']).execute()
            else:
                self.log("Nenhum backup anterior encontrado")
                
            self.progress["value"] = 70
            
            self.log("Iniciando upload para o Google Drive...")
            
            arquivo_metada = {
                'name': backup_filename
            }
            
            media = MediaFileUpload(
                backup_path,
                resumable=True
            )
            
            file = service.files().create(
                body=arquivo_metada,
                media_body=media,
                fields='id,name'
            ).execute()
            
            self.log(f"Upload concluído! ID do arquivo: {file.get('id')}")
            self.progress["value"] = 100
            self.status_var.set("Backup concluído com sucesso!")
            
            media._fd.close()
            
            import time
            time.sleep(3)
            
            max_attempts = 3
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    if os.path.exists(backup_path):
                        import gc
                        gc.collect()
                        os.chmod(backup_path, 0o777) 
                        os.unlink(backup_path)
                        self.log("Arquivo ZIP local removido")
                        break
                except PermissionError:
                    attempt += 1
                    self.log(f"Tentativa {attempt} de remover arquivo falhou, aguardando...")
                    time.sleep(2) 
                except Exception as e:
                    self.log(f"Erro ao remover arquivo: {e}")
                    break
            
            if attempt == max_attempts:
                self.log("Não foi possível remover o arquivo ZIP automaticamente.")
                self.log(f"Por favor, remova manualmente: {backup_path}")
            
            messagebox.showinfo("Backup Concluído", "Backup do Obsidian Vault realizado com sucesso!")
            
        except Exception as e:
            self.log(f"ERRO durante o backup: {e}")
            messagebox.showerror("Erro", f"Erro durante o backup: {e}")
            self.status_var.set("Erro no backup")

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Obsidian Vault Backup Tool')
    parser.add_argument('--run', action='store_true', help='Executa o backup imediatamente sem interface gráfica')
    return parser.parse_args()

def run_headless_backup():
    print("Executando backup do Obsidian Vault...")

    try:
        from fileZip import get_arquivo, get_backup_path
        from connectDrive import get_drive_service
        from googleapiclient.http import MediaFileUpload
        import shutil
        import os
        
        # Verificar e criar backup
        documents_path = os.path.expanduser("~\\Documents")
        obsidian_folder = "Obsidian Vault"
        vault_path = os.path.join(documents_path, obsidian_folder)
        
        if not os.path.exists(vault_path):
            print(f"Erro: Vault do Obsidian não encontrado em: {vault_path}")
            sys.exit(1)
            
        backup_filename = get_arquivo()
        backup_path = get_backup_path()
        
        print(f"Criando arquivo ZIP: {backup_filename}")
        shutil.make_archive(
            os.path.splitext(backup_path)[0], 'zip', vault_path
        )
        
        service = get_drive_service()
        
        print("Verificando backups anteriores...")
        prefixo = "Obsidian_Vault"
        pesquisa = f"name contains '{prefixo}' and trashed = false"
        
        results = service.files().list(
            q=pesquisa,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        arquivos_encontrados = results.get('files', [])
        
        if arquivos_encontrados:
            print(f"Removendo {len(arquivos_encontrados)} backups anteriores...")
            for arquivo in arquivos_encontrados:
                service.files().delete(fileId=arquivo['id']).execute()
        
        print("Iniciando upload para o Google Drive...")
        arquivo_metada = {'name': backup_filename}
        media = MediaFileUpload(backup_path, resumable=True)
        
        file = service.files().create(
            body=arquivo_metada,
            media_body=media,
            fields='id,name'
        ).execute()
        
        print(f"Upload concluído! ID do arquivo: {file.get('id')}")
        
        try:
            os.remove(backup_path)
            print("Arquivo ZIP local removido")
        except Exception as e:
            print(f"Aviso: Não foi possível remover o arquivo ZIP local: {e}")
        
        print("Backup concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante o backup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    args = parse_args()
    
    if args.run:
        run_headless_backup()
    else:
        app = ObsidianBackupTool()
        app.setup_gui()