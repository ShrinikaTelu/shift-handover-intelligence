# Frontend Quick Start
# Run from the frontend/ folder

Write-Host "🚀 Starting Shift Handover Intelligence Frontend" -ForegroundColor Cyan

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Starting Angular dev server on http://localhost:4200" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

ng serve --open
