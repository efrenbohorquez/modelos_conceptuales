# Script de PowerShell para iniciar el Dashboard de Modelos Conceptuales
# Archivo: run_dashboard.ps1

Write-Host "🚀 Iniciando Dashboard de Modelos Conceptuales de Supermercado" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Blue

# Verificar que estamos en el directorio correcto
$currentDir = Get-Location
Write-Host "📁 Directorio actual: $currentDir" -ForegroundColor Yellow

# Verificar archivos principales
$requiredFiles = @("app.py", "requirements.txt", "src/eda.py")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Archivo encontrado: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Archivo faltante: $file" -ForegroundColor Red
        exit 1
    }
}

# Verificar e instalar dependencias
Write-Host "`n🔧 Verificando dependencias..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt | Out-Null
    Write-Host "✅ Dependencias verificadas/instaladas" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Advertencia: Error al verificar dependencias" -ForegroundColor Yellow
}

# Verificar datos de prueba
$dataFiles = @("data/test_supermarket_data.csv", "data/clientes_info.csv")
foreach ($file in $dataFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Datos de prueba encontrados: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Datos de prueba no encontrados: $file" -ForegroundColor Yellow
    }
}

Write-Host "`n🌐 Iniciando servidor Streamlit..." -ForegroundColor Cyan
Write-Host "📱 El dashboard se abrirá en: http://localhost:8506" -ForegroundColor Magenta
Write-Host "🛑 Para detener el servidor, presiona Ctrl+C" -ForegroundColor Yellow
Write-Host "`n" + "=" * 60 -ForegroundColor Blue

# Iniciar Streamlit
streamlit run app.py --server.port 8506
