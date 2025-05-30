# Script PowerShell optimizado para ejecutar el dashboard
Write-Host "🚀 DASHBOARD MODELOS CONCEPTUALES SUPERMERCADO" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

# Cambiar al directorio
Set-Location "c:\Users\Public\modelos_conceptuales"
Write-Host "📁 Directorio: $(Get-Location)" -ForegroundColor Yellow

# Verificar archivos
if (Test-Path "app.py") {
    Write-Host "✅ app.py encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ app.py NO encontrado" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}

# Mostrar información
Write-Host ""
Write-Host "🌐 Iniciando Streamlit..." -ForegroundColor Cyan
Write-Host "🔗 URL: http://localhost:8509" -ForegroundColor Yellow
Write-Host "⏳ Cargando... (puede tomar unos segundos)" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Para detener: Presiona Ctrl+C" -ForegroundColor Gray
Write-Host ""

# Ejecutar Streamlit
try {
    streamlit run app.py --server.port 8509
} catch {
    Write-Host "❌ Error al ejecutar Streamlit: $_" -ForegroundColor Red
    Write-Host "💡 Verifica que Streamlit esté instalado: pip install streamlit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🛑 Dashboard detenido" -ForegroundColor Red
Read-Host "Presiona Enter para salir"
