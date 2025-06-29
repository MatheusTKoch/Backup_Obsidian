@echo off
echo =====================================
echo  Obsidian Backup Tool Installer
echo =====================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Este script precisa ser executado como Administrador.
    echo Clique com o botao direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

:: Set installation directory
set "INSTALL_DIR=%ProgramFiles%\Obsidian Backup Tool"

echo Instalando Obsidian Backup Tool...
echo.

:: Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo ✓ Diretorio de instalacao criado: %INSTALL_DIR%
) else (
    echo ✓ Diretorio de instalacao existe: %INSTALL_DIR%
)

:: Detect architecture and copy appropriate executable
if exist "%SYSTEMROOT%\SysWOW64" (
    echo ✓ Sistema 64-bit detectado
    if exist "ObsidianBackup_x64.exe" (
        copy "ObsidianBackup_x64.exe" "%INSTALL_DIR%\ObsidianBackup.exe" >nul
        echo ✓ Executavel 64-bit copiado
    ) else (
        echo ❌ Executavel 64-bit nao encontrado
        goto :error
    )
) else (
    echo ✓ Sistema 32-bit detectado
    if exist "ObsidianBackup_x86.exe" (
        copy "ObsidianBackup_x86.exe" "%INSTALL_DIR%\ObsidianBackup.exe" >nul
        echo ✓ Executavel 32-bit copiado
    ) else (
        echo ❌ Executavel 32-bit nao encontrado
        goto :error
    )
)

:: Create desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\Obsidian Backup Tool.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\ObsidianBackup.exe'; $Shortcut.Save()"

if exist "%SHORTCUT%" (
    echo ✓ Atalho criado na area de trabalho
) else (
    echo ⚠ Nao foi possivel criar o atalho na area de trabalho
)

:: Create start menu shortcut
set "STARTMENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs"
set "STARTSHORTCUT=%STARTMENU%\Obsidian Backup Tool.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTSHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\ObsidianBackup.exe'; $Shortcut.Save()"

if exist "%STARTSHORTCUT%" (
    echo ✓ Atalho criado no menu iniciar
) else (
    echo ⚠ Nao foi possivel criar o atalho no menu iniciar
)

echo.
echo =====================================
echo  Instalacao Concluida!
echo =====================================
echo.
echo O Obsidian Backup Tool foi instalado em:
echo %INSTALL_DIR%
echo.
echo Voce pode executar o programa:
echo - Atraves do atalho na area de trabalho
echo - Atraves do menu iniciar
echo - Diretamente do diretorio de instalacao
echo.

:: Ask if user wants to run the program now
set /p "run=Deseja executar o programa agora? (s/n): "
if /i "%run%"=="s" (
    start "" "%INSTALL_DIR%\ObsidianBackup.exe"
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul
exit /b 0

:error
echo.
echo ❌ Erro na instalacao!
echo Verifique se os arquivos executaveis estao no mesmo diretorio que este instalador.
echo.
pause
exit /b 1
