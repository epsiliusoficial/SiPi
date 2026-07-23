@echo off
if not exist "%~dp0editor_protegido.py" (
    echo [SiPi] Error: no se encontro editor_protegido.py en esta carpeta.
    pause
    exit /b
)
python "%~dp0editor_protegido.py"
