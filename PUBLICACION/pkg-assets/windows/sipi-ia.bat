@echo off
rem Wrapper de SiPi IA Agente para Windows (linea de comandos / herramienta para otras IAs).
setlocal
set AQUI=%~dp0
python "%AQUI%sipi_ia_agente.py" %*
