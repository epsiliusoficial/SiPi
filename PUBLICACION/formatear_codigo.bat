@echo off
title SiPi - Formatear codigo
if "%~1"=="" (
    echo Uso: formatear_codigo.bat archivo.sipi
    pause
    exit /b
)
python "%~dp0sipi.py" --formatear %1
pause
