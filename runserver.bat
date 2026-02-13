@echo off
REM Script para iniciar el servidor de desarrollo en Windows
REM Uso: runserver.bat

setlocal enabledelayedexpansion

REM Obtener el directorio actual
set SCRIPT_DIR=%~dp0

REM Cambiar al directorio del proyecto
cd /d "%SCRIPT_DIR%"

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar el servidor
python manage.py runserver

REM Pausa para ver mensajes de error si los hay
pause
