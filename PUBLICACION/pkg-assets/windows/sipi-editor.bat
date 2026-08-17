@echo off
rem Wrapper del editor visual de SiPi para Windows (requiere Python con Tk,
rem incluido por defecto en el instalador oficial de python.org).
setlocal
set AQUI=%~dp0
chcp 65001 >nul
if exist "%AQUI%editor_sipi.py" (
    python "%AQUI%editor_sipi.py" %*
) else if exist "%AQUI%editor_protegido.py" (
    python "%AQUI%editor_protegido.py" %*
) else (
    echo [SiPi] No se encontro editor_sipi.py ni editor_protegido.py junto a sipi-editor.bat.
    exit /b 1
)
