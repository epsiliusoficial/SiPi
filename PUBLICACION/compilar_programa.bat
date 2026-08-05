@echo off
title SiPi - Compilar a .exe
if "%~1"=="" (
    echo Uso: compilar_programa.bat archivo.sipi
    echo Ejemplo: compilar_programa.bat ejemplos\hola_mundo.sipi
    pause
    exit /b
)
if not exist "%~dp0generar_exe_protegido.py" (
    echo [SiPi] Error: no se encontro generar_exe_protegido.py en esta carpeta.
    pause
    exit /b
)
python "%~dp0generar_exe_protegido.py" %1
pause
