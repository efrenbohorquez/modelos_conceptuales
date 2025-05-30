# Script de PowerShell para ejecutar el dashboard corregido
# Archivo: restart_dashboard.ps1

Write-Host "🔄 Reiniciando Dashboard de Streamlit..." -ForegroundColor Cyan

# Detener procesos de Python existentes que puedan estar ejecutando Streamlit
Write-Host "⏹️  Deteniendo procesos existentes..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force

# Esperar un momento
Start-Sleep -Seconds 2

# Navegar al directorio del proyecto
Set-Location "c:\Users\Public\modelos_conceptuales"

# Ejecutar Streamlit
Write-Host "🚀 Iniciando Streamlit en puerto 8507..." -ForegroundColor Green
streamlit run app.py --server.port 8507

Write-Host "✅ Dashboard iniciado en http://localhost:8507" -ForegroundColor Green
