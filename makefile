# Makefile para Obsidian Backup Tool

APP_NAME = Obsidian_Backup_Tool
VERSION = 1.0.1
PYTHON = C:/Python313/python.exe
BUILD_DIR = build
DIST_DIR = dist
RELEASE_DIR = release
EXE_64 = ObsidianBackup_x64.exe
EXE_32 = ObsidianBackup_x86.exe

.PHONY: all quick clean setup install_deps build build_64 build_32 release test help

# Build completo
all: clean setup build release

# Build rápido usando script Python
quick: clean install_deps
	@echo Construindo executáveis...
	@$(PYTHON) build.py

# Criar diretórios
setup:
	@if not exist "$(BUILD_DIR)" mkdir "$(BUILD_DIR)" >nul 2>&1
	@if not exist "$(DIST_DIR)" mkdir "$(DIST_DIR)" >nul 2>&1
	@if not exist "$(RELEASE_DIR)" mkdir "$(RELEASE_DIR)" >nul 2>&1

# Instalar dependências
install_deps:
	@echo Instalando dependências...
	@$(PYTHON) -m pip install -r requirements.txt >nul

# Build manual (ambos)
build: build_64 build_32

# Build 64-bit
build_64:
	@echo Construindo executável 64-bit...
	@$(PYTHON) -m PyInstaller obsidian_backup_x64.spec --clean >nul
	@if exist "dist\$(EXE_64)" (echo ✓ 64-bit concluído) else (echo ❌ Falha 64-bit)

# Build 32-bit
build_32:
	@echo Construindo executável 32-bit...
	@$(PYTHON) -m PyInstaller obsidian_backup_x86.spec --clean >nul
	@if exist "dist\$(EXE_32)" (echo ✓ 32-bit concluído) else (echo ❌ Falha 32-bit)

# Criar pacote de release
release:
	@echo Criando pacote de release...
	@$(PYTHON) release.py --create-zip >nul
	@$(PYTHON) prepare_release.py >nul
	@echo ✓ Release preparado

# Limpar arquivos
clean:
	@if exist "$(BUILD_DIR)" rmdir /s /q "$(BUILD_DIR)" 2>nul
	@if exist "$(DIST_DIR)" rmdir /s /q "$(DIST_DIR)" 2>nul
	@if exist "__pycache__" rmdir /s /q "__pycache__" 2>nul
	@if exist "*.pyc" del /q "*.pyc" 2>nul

# Testar executáveis
test:
	@if exist "dist\$(EXE_64)" (echo ✓ 64-bit OK) else (echo ❌ 64-bit ausente)
	@if exist "dist\$(EXE_32)" (echo ✓ 32-bit OK) else (echo ❌ 32-bit ausente)

# Ajuda
help:
	@echo Comandos disponíveis:
	@echo   all        - Build completo (limpar + construir + release)
	@echo   quick      - Build rápido usando script Python
	@echo   build      - Construir ambos executáveis
	@echo   build_64   - Construir apenas 64-bit
	@echo   build_32   - Construir apenas 32-bit
	@echo   release    - Criar pacote de release
	@echo   clean      - Limpar arquivos de build
	@echo   test       - Verificar executáveis
	@echo   help       - Mostrar esta ajuda
