@echo off
echo Compilando aplicacion .exe real con PyInstaller...
pip install pyinstaller
pyinstaller --onefile --windowed app.py
echo.
echo Listo. El archivo .exe real esta en la carpeta "dist".
pause
