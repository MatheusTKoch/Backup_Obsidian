#!/usr/bin/env python3
"""
Preparador de Release para Obsidian Backup Tool
Cria arquivos necessários para release no GitHub
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def create_github_release_files():
    """Criar arquivos necessários para release no GitHub"""
    
    print("Preparando release...")
    
    version = "1.0.1"
    app_name = "Obsidian_Backup_Tool"
    release_dir = Path("release")
    
    if not release_dir.exists():
        print("❌ Pasta release não encontrada")
        return False
    
    files = list(release_dir.glob("*"))
    if not files:
        print("❌ Nenhum arquivo encontrado")
        return False
    
    total_size = 0
    for file_path in files:
        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            total_size += size_mb
    
    print(f"📊 {len(files)} arquivos ({total_size:.1f} MB)")
    
    # Criar notas de release
    release_notes_path = release_dir / "RELEASE_NOTES.md"
    with open(release_notes_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Obsidian Backup Tool v{version}

## 🎉 Novo Release

Esta versão inclui executáveis para sistemas Windows de 32 e 64 bits com instalador automático.

## 📦 Downloads Disponíveis

### Instalação Recomendada
- **Obsidian_Backup_Tool_v{version}_Complete.zip** - Pacote completo com instalador automático

### Downloads Individuais
- **ObsidianBackup_x64.exe** - Para sistemas Windows 64-bit
- **ObsidianBackup_x86.exe** - Para sistemas Windows 32-bit
- **install.bat** - Script de instalação automática

## 🛠 Instalação

### Método 1: Instalação Automática (Recomendado)
1. Baixe o arquivo `Obsidian_Backup_Tool_v{version}_Complete.zip`
2. Extraia todos os arquivos para uma pasta temporária
3. Execute `install.bat` **como Administrador**
4. Siga as instruções na tela

### Método 2: Instalação Manual
1. Baixe o executável apropriado para seu sistema
2. Execute diretamente ou copie para uma pasta de sua escolha

## 🚀 Funcionalidades

- ✅ Interface gráfica intuitiva para configuração
- ✅ Backup manual com um clique
- ✅ Agendamento de backups automáticos
- ✅ Upload direto para Google Drive
- ✅ Gerenciamento de versões anteriores
- ✅ Suporte completo para Obsidian Vaults
- ✅ Instalador automático para Windows

## 📋 Requisitos

- **Sistema**: Windows 7 ou superior
- **Arquitetura**: 32-bit ou 64-bit
- **Internet**: Para upload ao Google Drive
- **Google Account**: Para acesso ao Google Drive

## 🔧 Melhorias nesta Versão

- ✅ Correção dos problemas de geração de executáveis
- ✅ Novos executáveis otimizados para 32 e 64 bits
- ✅ Instalador automático incluído
- ✅ Guia de instalação detalhado
- ✅ Melhor compatibilidade com diferentes versões do Windows

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/MatheusTKoch/Backup_Obsidian/issues)
- **Documentação**: Veja INSTALL.md no pacote

## 🔄 Atualização

Se você já tem uma versão anterior instalada:
1. Feche o programa atual
2. Baixe a nova versão
3. Execute o instalador ou substitua o executável

---
**Versão**: {version}  
**Data**: 29/06/2025
""")
    
    # Criar instruções de upload
    upload_instructions = release_dir / "UPLOAD_INSTRUCTIONS.md"
    with open(upload_instructions, 'w', encoding='utf-8') as f:
        f.write(f"""# Instruções para Upload no GitHub

## 📤 Como fazer o release no GitHub:

### 1. Via Interface Web (Recomendado)

1. Acesse: https://github.com/MatheusTKoch/Backup_Obsidian/releases/new

2. Preencha os campos:
   - **Tag version**: `v{version}`
   - **Release title**: `Obsidian Backup Tool v{version}`
   - **Description**: Copie o conteúdo de RELEASE_NOTES.md

3. Faça upload dos seguintes arquivos:
   - `Obsidian_Backup_Tool_v{version}_Complete.zip` (Pacote principal)
   - `ObsidianBackup_x64.exe` (Executável 64-bit)
   - `ObsidianBackup_x86.exe` (Executável 32-bit)

4. Marque como "Latest release"

5. Clique em "Publish release"

### 2. Via GitHub CLI (Opcional)

```bash
git tag v{version}
git push origin v{version}

gh release create v{version} \\
  --title "Obsidian Backup Tool v{version}" \\
  --notes-file RELEASE_NOTES.md \\
  --latest \\
  release/Obsidian_Backup_Tool_v{version}_Complete.zip \\
  release/ObsidianBackup_x64.exe \\
  release/ObsidianBackup_x86.exe
```

### 3. Verificação

- [ ] Release publicado
- [ ] Downloads funcionando
- [ ] Executáveis testados

""")
    
    # Criar checksums
    import hashlib
    checksums_path = release_dir / "CHECKSUMS.txt"
    with open(checksums_path, 'w', encoding='utf-8') as f:
        f.write(f"# Checksums Obsidian Backup Tool v{version}\n")
        f.write(f"# Gerado em: 29/06/2025\n\n")
        
        for file_path in release_dir.glob("*.exe"):
            with open(file_path, 'rb') as file:
                sha256_hash = hashlib.sha256(file.read()).hexdigest()
                f.write(f"SHA256({file_path.name}) = {sha256_hash}\n")
        
        for file_path in release_dir.glob("*.zip"):
            with open(file_path, 'rb') as file:
                sha256_hash = hashlib.sha256(file.read()).hexdigest()
                f.write(f"SHA256({file_path.name}) = {sha256_hash}\n")
    
    print("✓ Arquivos de release criados")
    print(f"📁 {release_dir.absolute()}")
    print("\nPróximos passos:")
    print("1. Leia UPLOAD_INSTRUCTIONS.md")
    print("2. Crie release no GitHub")
    print("3. Faça upload dos arquivos")
    
    return True

if __name__ == "__main__":
    success = create_github_release_files()
    sys.exit(0 if success else 1)
