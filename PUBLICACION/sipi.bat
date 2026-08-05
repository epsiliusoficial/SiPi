@echo off
if "%~1"=="" (
    echo Uso: sipi.bat archivo.sipi
    pause
    exit /b
)
if not exist "%~dp0sipi_protegido.py" (
    echo [SiPi] Error: no se encontro sipi_protegido.py en esta carpeta.
    pause
    exit /b
)
python "%~dp0sipi_protegido.py" %1
pause
