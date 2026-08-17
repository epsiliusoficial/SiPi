@echo off
rem Wrapper de la CLI profesional de SiPi para Windows.
setlocal
set AQUI=%~dp0
python "%AQUI%sipi_cli.py" %*
