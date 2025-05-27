# Script de PowerShell para ejecutar el dashboard corregido
Write-Host "🚀 Iniciando Dashboard de Modelos Conceptuales..." -ForegroundColor Green

# Cambiar al directorio del proyecto
Set-Location "c:\Users\Public\modelos_conceptuales"

# Verificar que existe el archivo principal
if (Test-Path "app.py") {
    Write-Host "✅ Archivo app.py encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Archivo app.py no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar datos
if (Test-Path "data\test_supermarket_data.csv") {
    Write-Host "✅ Datos de prueba encontrados" -ForegroundColor Green
} else {
    Write-Host "❌ Datos de prueba no encontrados" -ForegroundColor Red
    exit 1
}

Write-Host "🔄 Ejecutando dashboard en puerto 8506..." -ForegroundColor Yellow
Write-Host "📍 URL: http://localhost:8506" -ForegroundColor Cyan
Write-Host "⏹️  Para detener: Ctrl+C" -ForegroundColor Yellow

# Ejecutar streamlit
streamlit run app.py --server.port 8506
