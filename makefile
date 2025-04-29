# Makefile for building PyInstaller executables, Inno Setup installers, and GitHub releases

# Application details
APP_NAME = Obsidian_Backup_Tool
VERSION = 1.0.0
MAIN_SCRIPT = main.py

# Python paths (update these paths to match your system)
PYTHON_64 = C:\Users\Matheus\AppData\Local\Programs\Python\Python312\python.exe
PYTHON_32 = C:\Users\Matheus\AppData\Local\Programs\Python\Python312\python.exe
PYTHON = python

# Inno Setup Compiler path
INNO_SETUP = "C:/Program Files (x86)/Inno Setup 6/ISCC.exe"

# Build directories
BUILD_DIR = build
DIST_DIR = dist
DIST_64 = $(DIST_DIR)/x64
DIST_32 = $(DIST_DIR)/x86
RELEASE_DIR = release

# Output names
EXE_64 = $(APP_NAME)_x64.exe
EXE_32 = $(APP_NAME)_x86.exe
SETUP_64 = $(APP_NAME)_x64_Setup.exe
SETUP_32 = $(APP_NAME)_x86_Setup.exe

# GitHub release settings
GITHUB_REPO = MatheusTKoch/Backup_Obsidian
GITHUB_TAG = v$(VERSION)
GITHUB_RELEASE_NAME = $(APP_NAME) $(VERSION)
GITHUB_RELEASE_BODY = "Release of $(APP_NAME) version $(VERSION) for both 32-bit and 64-bit systems."

# Default target
.PHONY: all
all: setup build_all installers

# Create output directories
.PHONY: setup
setup:
	@echo "Creating output directories..."
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(DIST_64)
	@mkdir -p $(DIST_32)
	@mkdir -p $(RELEASE_DIR)

# Build 64-bit executable
.PHONY: build_64
build_64:
	@echo "Building 64-bit executable..."
	@$(PYTHON_64) -m PyInstaller --onefile --clean --name $(EXE_64:%.exe=%) \
		--distpath $(DIST_64) --workpath $(BUILD_DIR)/x64 $(MAIN_SCRIPT)
	@echo "64-bit executable built successfully."

# Build 32-bit executable
.PHONY: build_32
build_32:
	@echo "Building 32-bit executable..."
	@$(PYTHON_32) -m PyInstaller --onefile --clean --name $(EXE_32:%.exe=%) \
		--distpath $(DIST_32) --workpath $(BUILD_DIR)/x32 $(MAIN_SCRIPT)
	@echo "32-bit executable built successfully."

# Build both executables
.PHONY: build_all
build_all: build_64 build_32

# Generate Inno Setup script for 64-bit
.PHONY: inno_script_64
inno_script_64:
	@echo "Generating 64-bit Inno Setup script..."
	@echo '#define MyAppName "$(APP_NAME)"' > inno_setup_x64.iss
	@echo '#define MyAppVersion "$(VERSION)"' >> inno_setup_x64.iss
	@echo '#define MyAppPublisher "Your Name or Company"' >> inno_setup_x64.iss
	@echo '#define MyAppURL "https://github.com/$(GITHUB_REPO)"' >> inno_setup_x64.iss
	@echo '#define MyAppExeName "$(EXE_64)"' >> inno_setup_x64.iss
	@echo '' >> inno_setup_x64.iss
	@echo '[Setup]' >> inno_setup_x64.iss
	@echo 'AppId={{YOUR-UNIQUE-APP-ID-HERE}' >> inno_setup_x64.iss
	@echo 'AppName={#MyAppName}' >> inno_setup_x64.iss
	@echo 'AppVersion={#MyAppVersion}' >> inno_setup_x64.iss
	@echo 'AppPublisher={#MyAppPublisher}' >> inno_setup_x64.iss
	@echo 'AppPublisherURL={#MyAppURL}' >> inno_setup_x64.iss
	@echo 'AppSupportURL={#MyAppURL}' >> inno_setup_x64.iss
	@echo 'AppUpdatesURL={#MyAppURL}' >> inno_setup_x64.iss
	@echo 'DefaultDirName={autopf}\{#MyAppName}' >> inno_setup_x64.iss
	@echo 'DefaultGroupName={#MyAppName}' >> inno_setup_x64.iss
	@echo 'OutputBaseFilename=$(SETUP_64:%.exe=%)' >> inno_setup_x64.iss
	@echo 'OutputDir=$(RELEASE_DIR)' >> inno_setup_x64.iss
	@echo 'Compression=lzma' >> inno_setup_x64.iss
	@echo 'SolidCompression=yes' >> inno_setup_x64.iss
	@echo 'ArchitecturesInstallIn64BitMode=x64' >> inno_setup_x64.iss
	@echo 'ArchitecturesAllowed=x64' >> inno_setup_x64.iss
	@echo '' >> inno_setup_x64.iss
	@echo '[Languages]' >> inno_setup_x64.iss
	@echo 'Name: "english"; MessagesFile: "compiler:Default.isl"' >> inno_setup_x64.iss
	@echo '' >> inno_setup_x64.iss
	@echo '[Tasks]' >> inno_setup_x64.iss
	@echo 'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked' >> inno_setup_x64.iss
	@echo '' >> inno_setup_x64.iss
	@echo '[Files]' >> inno_setup_x64.iss
	@echo 'Source: "$(DIST_64)\$(EXE_64)"; DestDir: "{app}"; Flags: ignoreversion' >> inno_setup_x64.iss
	@echo '; Add any additional files needed by your application' >> inno_setup_x64.iss
	@echo '' >> inno_setup_x64.iss
	@echo '[Icons]' >> inno_setup_x64.iss
	@echo 'Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"' >> inno_setup_x64.iss
	@echo 'Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"' >> inno_setup_x64.iss
	@echo 'Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon' >> inno_setup_x64.iss
	@echo '' >> inno_setup_x64.iss
	@echo '[Run]' >> inno_setup_x64.iss
	@echo 'Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent' >> inno_setup_x64.iss

# Generate Inno Setup script for 32-bit
.PHONY: inno_script_32
inno_script_32:
	@echo "Generating 32-bit Inno Setup script..."
	@echo '#define MyAppName "$(APP_NAME)"' > inno_setup_x86.iss
	@echo '#define MyAppVersion "$(VERSION)"' >> inno_setup_x86.iss
	@echo '#define MyAppPublisher "Your Name or Company"' >> inno_setup_x86.iss
	@echo '#define MyAppURL "https://github.com/$(GITHUB_REPO)"' >> inno_setup_x86.iss
	@echo '#define MyAppExeName "$(EXE_32)"' >> inno_setup_x86.iss
	@echo '' >> inno_setup_x86.iss
	@echo '[Setup]' >> inno_setup_x86.iss
	@echo 'AppId={{YOUR-UNIQUE-APP-ID-HERE-32BIT}' >> inno_setup_x86.iss
	@echo 'AppName={#MyAppName}' >> inno_setup_x86.iss
	@echo 'AppVersion={#MyAppVersion}' >> inno_setup_x86.iss
	@echo 'AppPublisher={#MyAppPublisher}' >> inno_setup_x86.iss
	@echo 'AppPublisherURL={#MyAppURL}' >> inno_setup_x86.iss
	@echo 'AppSupportURL={#MyAppURL}' >> inno_setup_x86.iss
	@echo 'AppUpdatesURL={#MyAppURL}' >> inno_setup_x86.iss
	@echo 'DefaultDirName={autopf}\{#MyAppName}' >> inno_setup_x86.iss
	@echo 'DefaultGroupName={#MyAppName}' >> inno_setup_x86.iss
	@echo 'OutputBaseFilename=$(SETUP_32:%.exe=%)' >> inno_setup_x86.iss
	@echo 'OutputDir=$(RELEASE_DIR)' >> inno_setup_x86.iss
	@echo 'Compression=lzma' >> inno_setup_x86.iss
	@echo 'SolidCompression=yes' >> inno_setup_x86.iss
	@echo 'ArchitecturesAllowed=x86 x64' >> inno_setup_x86.iss
	@echo '' >> inno_setup_x86.iss
	@echo '[Languages]' >> inno_setup_x86.iss
	@echo 'Name: "english"; MessagesFile: "compiler:Default.isl"' >> inno_setup_x86.iss
	@echo '' >> inno_setup_x86.iss
	@echo '[Tasks]' >> inno_setup_x86.iss
	@echo 'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked' >> inno_setup_x86.iss
	@echo '' >> inno_setup_x86.iss
	@echo '[Files]' >> inno_setup_x86.iss
	@echo 'Source: "$(DIST_32)\$(EXE_32)"; DestDir: "{app}"; Flags: ignoreversion' >> inno_setup_x86.iss
	@echo '; Add any additional files needed by your application' >> inno_setup_x86.iss
	@echo '' >> inno_setup_x86.iss
	@echo '[Icons]' >> inno_setup_x86.iss
	@echo 'Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"' >> inno_setup_x86.iss
	@echo 'Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"' >> inno_setup_x86.iss
	@echo 'Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon' >> inno_setup_x86.iss
	@echo '' >> inno_setup_x86.iss
	@echo '[Run]' >> inno_setup_x86.iss
	@echo 'Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent' >> inno_setup_x86.iss

# Build Inno Setup installers
.PHONY: build_installer_64
build_installer_64: inno_script_64
	@echo "Building 64-bit installer..."
	@$(INNO_SETUP) "inno_setup_x64.iss"
	@echo "64-bit installer built successfully."

.PHONY: build_installer_32
build_installer_32: inno_script_32
	@echo "Building 32-bit installer..."
	@$(INNO_SETUP) "inno_setup_x86.iss"
	@echo "32-bit installer built successfully."

# Build both installers
.PHONY: installers
installers: build_installer_64 build_installer_32
