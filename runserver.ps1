# Script PowerShell para ejecutar el servidor de desarrollo
# Uso: .\runserver.ps1

# Obtener el directorio del script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Cambiar al directorio del proyecto
Set-Location $ScriptDir

# Mensaje de bienvenida
Write-Host "===============================================" -ForegroundColor Green
Write-Host "🔧 Valser Portal - Servidor de Desarrollo" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "❌ Error: El entorno virtual no existe." -ForegroundColor Red
    Write-Host "Ejecuta primero: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activar el entorno virtual
Write-Host "✓ Activando entorno virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Nota: No se pudo activar el script de PowerShell (política de ejecución)." -ForegroundColor Yellow
    Write-Host "   Usaremos el ejecutable directo de Python." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✓ Iniciando servidor..." -ForegroundColor Cyan
Write-Host "   URL: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "   Admin: http://127.0.0.1:8000/admin" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona CTRL+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Ejecutar el servidor
& ".\venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
