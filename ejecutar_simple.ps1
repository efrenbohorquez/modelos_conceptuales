# Script PowerShell para ejecutar Streamlit de forma simple
Write-Host "🚀 Ejecutando Dashboard Final" -ForegroundColor Green

# Cambiar al directorio
Set-Location "c:\Users\Public\modelos_conceptuales"

# Ejecutar Streamlit
Write-Host "🌐 Iniciando en http://localhost:8508" -ForegroundColor Cyan
Start-Process "streamlit" -ArgumentList "run", "app.py", "--server.port", "8508" -NoNewWindow

Write-Host "✅ Dashboard ejecutándose en puerto 8508" -ForegroundColor Green
Write-Host "🔗 Para Streamlit Cloud: sube este proyecto a GitHub" -ForegroundColor Yellow

# Abrir navegador después de unos segundos
Start-Sleep -Seconds 3
Start-Process "http://localhost:8508"
