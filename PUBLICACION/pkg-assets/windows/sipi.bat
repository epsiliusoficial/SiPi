@echo off
rem Wrapper del interprete SiPi para Windows. Busca 'sipi.py' junto a este
rem .bat (carpeta de instalacion); si no esta (carpeta de publicacion sin
rem fuente), usa 'sipi_protegido.py' generado por herramientas\proteger_codigo.py.
setlocal
set AQUI=%~dp0
if exist "%AQUI%sipi.py" (
    python "%AQUI%sipi.py" %*
) else if exist "%AQUI%sipi_protegido.py" (
    python "%AQUI%sipi_protegido.py" %*
) else (
    echo [SiPi] No se encontro sipi.py ni sipi_protegido.py junto a sipi.bat.
    exit /b 1
)
