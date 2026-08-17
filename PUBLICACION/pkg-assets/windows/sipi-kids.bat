@echo off
rem Wrapper de SiPi Kids para Windows.
setlocal
set AQUI=%~dp0
chcp 65001 >nul
python "%AQUI%editor_sipi_kids.py" %*
