@echo off
title Instalador de SiPi
color 0B
echo ============================================
echo   SiPi - Instalador para Windows 10
echo ============================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo No se encontro Python instalado en este equipo.
    echo.
    echo Se abrira la pagina de descarga de Python.
    echo IMPORTANTE: durante la instalacion, marca la casilla
    echo "Add Python to PATH" antes de darle a Instalar.
    echo Tambien asegurate de que "tcl/tk and IDLE" quede tildado,
    echo si no el editor visual de SiPi no va a funcionar.
    start https://www.python.org/downloads/
    pause
    exit /b
)

echo Python encontrado correctamente.
echo.
echo Instalando/actualizando componentes de SiPi...
echo   - pygame        (para juegos)
echo   - pyinstaller   (para compilar a .exe)
echo   - Pillow        (para imagenes)
echo.
python -m pip install --upgrade pip --quiet
pip install pygame pyinstaller Pillow --quiet
echo.
echo ============================================
echo   Instalacion completada.
echo   Ya podes usar SiPi con "sipi.bat archivo.sipi"
echo   o abrir el editor visual con "editor.bat"
echo ============================================
pause
