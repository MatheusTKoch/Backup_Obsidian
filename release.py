#!/usr/bin/env python3
"""
Release script for Obsidian Backup Tool
Creates GitHub releases with the generated executables
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

class ReleaseManager:
    def __init__(self):
        self.app_name = "Obsidian_Backup_Tool"
        self.version = "1.0.1"
        self.release_dir = Path("release")
        self.github_repo = "MatheusTKoch/Backup_Obsidian"
        
    def get_release_info(self):
        """Get release information"""
        return {
            "tag": f"v{self.version}",
            "name": f"{self.app_name} v{self.version}",
            "body": self.get_release_notes(),
            "draft": False,
            "prerelease": False
        }
    
    def get_release_notes(self):
        """Generate release notes"""
        return f"""## {self.app_name} v{self.version}

### 🎉 New Release

Esta versão inclui executáveis para sistemas Windows de 32 e 64 bits.

### 📦 Downloads Disponíveis

- **ObsidianBackup_x64.exe** - Para sistemas Windows 64-bit
- **ObsidianBackup_x86.exe** - Para sistemas Windows 32-bit

### 🚀 Funcionalidades

- Interface gráfica intuitiva para configuração
- Backup manual com um clique
- Agendamento de backups automáticos
- Upload direto para Google Drive
- Gerenciamento de versões anteriores
- Suporte completo para Obsidian Vaults

### 🔧 Instalação

1. Baixe o executável apropriado para seu sistema (32 ou 64 bits)
2. Execute o arquivo `.exe` baixado
3. Siga as instruções de configuração no aplicativo

### 📋 Requisitos

- Windows 7 ou superior
- Conexão com a internet para upload ao Google Drive
- Conta do Google para acesso ao Google Drive

### 🛠 Problemas Corrigidos

- Melhorias na geração de executáveis
- Correções de compatibilidade com diferentes versões do Windows
- Otimizações de performance

### 📞 Suporte

Se encontrar problemas, por favor abra uma issue no GitHub.

---
**Data de Release:** {datetime.now().strftime("%d/%m/%Y")}
"""
    
    def check_executables(self):
        """Check if executables are available"""
        executables = [
            "ObsidianBackup_x64.exe",
            "ObsidianBackup_x86.exe"
        ]
        
        available = []
        missing = []
        
        for exe in executables:
            exe_path = self.release_dir / exe
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                available.append(f"{exe} ({size_mb:.1f} MB)")
            else:
                missing.append(exe)
        
        return available, missing
    
    def create_release_zip(self):
        """Create a ZIP file with all executables and installation files"""
        import zipfile
        
        zip_path = self.release_dir / f"{self.app_name}_v{self.version}_Complete.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add executables
            for exe_file in self.release_dir.glob("*.exe"):
                zipf.write(exe_file, exe_file.name)
                print(f"   ✓ Added {exe_file.name} to ZIP")
            
            # Add installer script if exists
            installer_path = self.release_dir / "install.bat"
            if installer_path.exists():
                zipf.write(installer_path, installer_path.name)
                print(f"   ✓ Added {installer_path.name} to ZIP")
            
            # Add installation guide if exists
            install_md_path = self.release_dir / "INSTALL.md"
            if install_md_path.exists():
                zipf.write(install_md_path, install_md_path.name)
                print(f"   ✓ Added {install_md_path.name} to ZIP")
            
            # Add release info
            info_path = self.release_dir / "release_info.json"
            if info_path.exists():
                zipf.write(info_path, info_path.name)
                print(f"   ✓ Added {info_path.name} to ZIP")
        
        return zip_path
    
    def generate_release_info_file(self):
        """Generate a JSON file with release information"""
        release_info = self.get_release_info()
        info_file = self.release_dir / "release_info.json"
        
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, indent=2, ensure_ascii=False)
        
        return info_file
    
    def show_release_summary(self):
        """Show release summary"""
        print(f"📋 Release Summary for {self.app_name} v{self.version}")
        print("=" * 60)
        
        available, missing = self.check_executables()
        
        if available:
            print("✅ Available executables:")
            for exe in available:
                print(f"   • {exe}")
        
        if missing:
            print("❌ Missing executables:")
            for exe in missing:
                print(f"   • {exe}")
        
        print(f"\n📁 Release directory: {self.release_dir.absolute()}")
        
        if available:
            print("\n🎯 Next steps:")
            print("1. Create ZIP package with: python release.py --create-zip")
            print("2. Upload to GitHub manually or use GitHub CLI")
            print("3. Tag the release with: git tag v{self.version}")
            print("4. Push tags: git push origin --tags")
        
        return len(available) > 0

def main():
    parser = argparse.ArgumentParser(description="Manage releases for Obsidian Backup Tool")
    parser.add_argument("--create-zip", action="store_true", help="Create ZIP package")
    parser.add_argument("--info", action="store_true", help="Generate release info JSON")
    parser.add_argument("--summary", action="store_true", help="Show release summary")
    
    args = parser.parse_args()
    
    manager = ReleaseManager()
    
    if args.create_zip:
        print("📦 Creating release ZIP package...")
        zip_path = manager.create_release_zip()
        print(f"   ✓ ZIP created: {zip_path}")
        return
    
    if args.info:
        print("📝 Generating release info...")
        info_file = manager.generate_release_info_file()
        print(f"   ✓ Release info saved: {info_file}")
        return
    
    if args.summary or not any([args.create_zip, args.info]):
        success = manager.show_release_summary()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
