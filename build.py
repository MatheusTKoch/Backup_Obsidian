#!/usr/bin/env python3
"""
Script de build para Obsidian Backup Tool
Gera executáveis 32-bit e 64-bit usando PyInstaller
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

class BuildManager:
    def __init__(self):
        self.app_name = "Obsidian_Backup_Tool"
        self.version = "1.0.1"
        self.python_exe = sys.executable
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.release_dir = Path("release")
        
    def clean(self):
        """Limpar diretórios de build"""
        print("Limpando arquivos...")
        
        directories_to_clean = [self.build_dir, self.dist_dir, "__pycache__"]
        for directory in directories_to_clean:
            if Path(directory).exists():
                try:
                    shutil.rmtree(directory)
                except Exception:
                    pass
        
        for pyc_file in Path(".").glob("**/*.pyc"):
            try:
                pyc_file.unlink()
            except Exception:
                pass
    
    def setup_directories(self):
        """Criar diretórios necessários"""
        directories = [self.build_dir, self.dist_dir, self.release_dir]
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    def install_dependencies(self):
        """Instalar dependências Python"""
        print("Instalando dependências...")
        
        if not Path("requirements.txt").exists():
            print("❌ requirements.txt não encontrado")
            return False
            
        try:
            subprocess.run([
                self.python_exe, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            return False
    
    def build_executable(self, architecture="x64"):
        """Construir executável para arquitetura especificada"""
        print(f"Construindo executável {architecture}...")
        
        spec_file = f"obsidian_backup_{architecture.lower()}.spec"
        if not Path(spec_file).exists():
            print(f"❌ Arquivo {spec_file} não encontrado")
            return False
        
        try:
            subprocess.run([
                self.python_exe, "-m", "PyInstaller", 
                spec_file, 
                "--clean", 
                "--noconfirm"
            ], capture_output=True, text=True, check=True)
            
            exe_name = f"ObsidianBackup_{architecture.lower()}.exe"
            exe_path = self.dist_dir / exe_name
            
            if exe_path.exists():
                print(f"✓ {architecture} concluído")
                return True
            else:
                print(f"❌ {architecture} falhou")
                return False
                
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao construir {architecture}")
            return False
    
    def prepare_release(self):
        """Copiar executáveis para diretório de release"""
        executables = [
            ("ObsidianBackup_x64.exe", "x64"),
            ("ObsidianBackup_x86.exe", "x86")
        ]
        
        copied_files = []
        for exe_name, arch in executables:
            src = self.dist_dir / exe_name
            dst = self.release_dir / exe_name
            
            if src.exists():
                try:
                    shutil.copy2(src, dst)
                    copied_files.append(exe_name)
                except Exception:
                    pass
        
        return len(copied_files) > 0
    
    def run_full_build(self):
        """Executar processo completo de build"""
        print(f"🚀 Build {self.app_name} v{self.version}")
        
        self.clean()
        self.setup_directories()
        
        if not self.install_dependencies():
            print("❌ Falha nas dependências")
            return False
        
        success_64 = self.build_executable("x64")
        success_32 = self.build_executable("x86")
        
        if not (success_64 or success_32):
            print("❌ Nenhum executável criado")
            return False
        
        if self.prepare_release():
            print("✓ Build concluído com sucesso")
            return True
        else:
            print("❌ Falha na preparação do release")
            return False

def main():
    parser = argparse.ArgumentParser(description="Build Obsidian Backup Tool")
    parser.add_argument("--clean", action="store_true", help="Apenas limpar")
    parser.add_argument("--install-deps", action="store_true", help="Apenas instalar dependências")
    parser.add_argument("--arch", choices=["x64", "x86", "both"], default="both", 
                        help="Arquitetura (padrão: both)")
    
    args = parser.parse_args()
    
    builder = BuildManager()
    
    if args.clean:
        builder.clean()
        return
    
    if args.install_deps:
        builder.install_dependencies()
        return
    
    if args.arch == "both":
        success = builder.run_full_build()
    else:
        builder.setup_directories()
        builder.install_dependencies()
        success = builder.build_executable(args.arch)
        if success:
            builder.prepare_release()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
