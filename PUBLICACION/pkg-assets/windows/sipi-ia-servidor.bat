@echo off
rem Wrapper del servidor HTTP de SiPi IA para Windows.
setlocal
set AQUI=%~dp0
python "%AQUI%sipi_ia_servidor.py" %*
